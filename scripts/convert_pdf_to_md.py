#!/usr/bin/env python3
"""
PDF to Markdown Converter using Marker with NVIDIA CUDA GPU Acceleration.
Optimized for NVIDIA GeForce RTX 4050 (Ada Lovelace, 6GB VRAM).

Converts scientific papers, theses, and documents into high-quality Markdown,
preserving headings, LaTeX math formulas, tables, and extracted figures.
"""

import argparse
import glob
import json
import os
import shutil
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Auto-reexec into project .venv if run with system python
try:
    import torch
    from marker.converters.pdf import PdfConverter
    from marker.models import create_model_dict
    from marker.output import save_output, text_from_rendered
    from tqdm import tqdm
except ImportError:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    venv_python = os.path.join(project_root, ".venv", "bin", "python")
    if os.path.exists(venv_python) and sys.executable != venv_python:
        os.execv(venv_python, [venv_python] + sys.argv)
    uv_bin = shutil.which("uv")
    if uv_bin:
        os.execv(uv_bin, ["uv", "run", "python"] + sys.argv)
    print("Error: Missing required packages (torch, marker-pdf, tqdm).")
    print("Please run using: uv run python " + " ".join(sys.argv))
    sys.exit(1)


# Global singleton for cached models in memory during batch processing
_CACHED_MODELS = None


def configure_gpu_environment() -> str:
    """Configures environment variables for NVIDIA CUDA inference."""
    os.environ["TORCH_DEVICE"] = "cuda"
    os.environ["INFERENCE_RAM"] = "6"  # 6GB VRAM allocation for RTX 4050
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        vram_gb = torch.cuda.get_device_properties(0).total_memory / (1024**3)
        return f"CUDA ({gpu_name}, {vram_gb:.2f} GB VRAM)"
    return "CPU (Peringatan: GPU CUDA tidak terdeteksi, berjalan lambat pada CPU)"


def get_marker_models(device: str = "cuda") -> Dict:
    """Loads and caches Marker models in memory, tuned for 6GB VRAM."""
    global _CACHED_MODELS
    if _CACHED_MODELS is None:
        configure_gpu_environment()
        is_cuda = torch.cuda.is_available() and device == "cuda"
        actual_device = "cuda" if is_cuda else "cpu"
        dtype = torch.float16 if is_cuda else torch.float32

        models = create_model_dict(device=actual_device, dtype=dtype)

        # Fine-tune batch sizes to avoid VRAM OOM on RTX 4050 6GB
        if is_cuda:
            if "layout_model" in models:
                models["layout_model"].batch_size = 4
            if "recognition_model" in models:
                models["recognition_model"].batch_size = 8
                if hasattr(models["recognition_model"], "foundation_predictor"):
                    fp = models["recognition_model"].foundation_predictor
                    fp.batch_size = 8
                    fp.encoder_chunk_sizes["cuda"] = 4096
            if "table_rec_model" in models:
                models["table_rec_model"].batch_size = 2
            if "detection_model" in models:
                models["detection_model"].batch_size = 4
            if "ocr_error_model" in models:
                models["ocr_error_model"].batch_size = 8

        _CACHED_MODELS = models
    return _CACHED_MODELS


def convert_pdf_to_markdown(
    pdf_path: str,
    output_base_dir: str = "literature/markdowns",
    page_range: Optional[List[int]] = None,
    models: Optional[Dict] = None,
    skip_existing: bool = True,
    device: str = "cuda",
) -> Optional[str]:
    """
    Converts a single PDF file to Markdown using Marker.

    Args:
        pdf_path: Absolute or relative path to the PDF file.
        output_base_dir: Base folder where the resulting markdown directory will be created.
        page_range: Optional list of page indices (0-indexed) to convert.
        models: Optional preloaded Marker model dictionary.
        skip_existing: If True, skips conversion if the output file already exists.
        device: 'cuda' or 'cpu'.

    Returns:
        Path to the generated markdown file, or None if conversion failed/skipped.
    """
    if not os.path.exists(pdf_path):
        print(f"[-] File tidak ditemukan: {pdf_path}")
        return None

    pdf_stem = Path(pdf_path).stem
    doc_out_dir = os.path.join(output_base_dir, pdf_stem)
    md_output_path = os.path.join(doc_out_dir, f"{pdf_stem}.md")

    if skip_existing and os.path.exists(md_output_path) and os.path.getsize(md_output_path) > 0:
        return md_output_path

    os.makedirs(doc_out_dir, exist_ok=True)

    try:
        if models is None:
            models = get_marker_models(device=device)

        config = {
            "recognition_batch_size": 8,
            "table_rec_batch_size": 2,
            "detection_batch_size": 4,
        }
        if page_range is not None:
            config["page_range"] = page_range

        converter = PdfConverter(
            artifact_dict=models,
            config=config,
        )

        rendered = converter(pdf_path)
        save_output(rendered, doc_out_dir, pdf_stem)

        if torch.cuda.is_available():
            torch.cuda.empty_cache()

        return md_output_path

    except Exception as e:
        print(f"[-] Gagal mengonversi '{pdf_path}' ke Markdown: {e}")
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        return None


def batch_convert(
    input_dir: str = "literature/pdfs",
    output_base_dir: str = "literature/markdowns",
    pattern: str = "*.pdf",
    skip_existing: bool = True,
    max_files: Optional[int] = None,
    page_range: Optional[List[int]] = None,
) -> List[str]:
    """Converts all PDFs matching pattern in input_dir to Markdown."""
    search_path = os.path.join(input_dir, pattern)
    pdf_files = sorted(glob.glob(search_path))

    if not pdf_files:
        print(f"[i] Tidak ada file PDF yang cocok di: {search_path}")
        return []

    if max_files:
        pdf_files = pdf_files[:max_files]

    device_info = configure_gpu_environment()
    print(f"[*] Perangkat Inferensi: {device_info}")
    print(f"[*] Memuat model Marker ke memori...")
    models = get_marker_models(device="cuda")

    print(f"[*] Menemukan {len(pdf_files)} file PDF untuk dikonversi.")
    converted_paths = []

    for pdf_path in tqdm(pdf_files, desc="Converting PDFs"):
        md_path = convert_pdf_to_markdown(
            pdf_path=pdf_path,
            output_base_dir=output_base_dir,
            page_range=page_range,
            models=models,
            skip_existing=skip_existing,
        )
        if md_path:
            converted_paths.append(md_path)

    print(f"\n[+] Selesai! {len(converted_paths)}/{len(pdf_files)} dokumen siap di: {output_base_dir}")
    return converted_paths


def parse_page_range_arg(arg: str) -> List[int]:
    """Parses range strings like '0-5', '0,2,4', '0-3,5' into a list of ints."""
    pages = set()
    parts = arg.split(",")
    for p in parts:
        p = p.strip()
        if "-" in p:
            start, end = p.split("-")
            pages.update(range(int(start), int(end) + 1))
        elif p.isdigit():
            pages.add(int(p))
    return sorted(list(pages))


def main():
    parser = argparse.ArgumentParser(
        description="Konversi dokumen PDF ke Markdown dengan Python Marker & Akselerasi GPU NVIDIA (RTX 4050)."
    )
    parser.add_argument(
        "--file",
        "-f",
        type=str,
        help="Path ke file PDF tunggal yang ingin dikonversi.",
    )
    parser.add_argument(
        "--dir",
        "-d",
        type=str,
        default="literature/pdfs",
        help="Direktori berisi file-file PDF (default: literature/pdfs).",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        type=str,
        default="literature/markdowns",
        help="Direktori dasar penyimpanan hasil Markdown (default: literature/markdowns).",
    )
    parser.add_argument(
        "--page-range",
        "-p",
        type=str,
        help="Rentang halaman yang ingin dikonversi (misal: '0-5' atau '0,1,2'). Default: seluruh dokumen.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Paksa konversi ulang meskipun file markdown sudah ada.",
    )
    parser.add_argument(
        "--limit",
        "-n",
        type=int,
        help="Batas maksimal jumlah file PDF yang diproses saat batch.",
    )
    parser.add_argument(
        "--check-gpu",
        action="store_true",
        help="Periksa ketersediaan dan status GPU NVIDIA tanpa melakukan konversi.",
    )

    args = parser.parse_args()

    # GPU Check
    device_info = configure_gpu_environment()
    if args.check_gpu:
        print(f"[+] Status GPU: {device_info}")
        if torch.cuda.is_available():
            print(f"    - Device Index  : 0")
            print(f"    - Device Name   : {torch.cuda.get_device_name(0)}")
            print(f"    - VRAM Total    : {torch.cuda.get_device_properties(0).total_memory / (1024**3):.2f} GB")
            print(f"    - VRAM Allocated: {torch.cuda.memory_allocated(0) / (1024**2):.2f} MB")
            print(f"    - CUDA Version  : {torch.version.cuda}")
        sys.exit(0)

    page_range = parse_page_range_arg(args.page_range) if args.page_range else None

    # Single file conversion
    if args.file:
        print(f"[*] Perangkat: {device_info}")
        start_time = time.time()
        print(f"[*] Mengonversi: {args.file}")
        if page_range:
            print(f"[*] Rentang halaman: {page_range}")
        out_md = convert_pdf_to_markdown(
            pdf_path=args.file,
            output_base_dir=args.output_dir,
            page_range=page_range,
            skip_existing=not args.force,
        )
        if out_md:
            elapsed = time.time() - start_time
            print(f"[+] Berhasil dikonversi dalam {elapsed:.2f} detik!")
            print(f"[+] Lokasi Markdown: {out_md}")
        else:
            print(f"[-] Konversi gagal.")
        sys.exit(0)

    # Batch directory conversion
    batch_convert(
        input_dir=args.dir,
        output_base_dir=args.output_dir,
        skip_existing=not args.force,
        max_files=args.limit,
        page_range=page_range,
    )


if __name__ == "__main__":
    main()
