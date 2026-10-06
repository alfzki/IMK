"""Synthesizer for research gaps, open problems, and novel research opportunities."""

from __future__ import annotations

import logging
from typing import Dict, List, Optional

from calm_carson.brainstorm.models import BrainstormClusterSummary, ResearchGapItem

logger = logging.getLogger(__name__)

CLUSTER_NAMES = {
    "security_privacy": "Keamanan Sistem & Privasi Data Statistik (SDC / Differential Privacy)",
    "sdi_interoperability": "Enterprise Architecture, Interoperabilitas & Satu Data Indonesia (SDI)",
    "data_collection_capi": "Sistem Pengumpulan Data Cerdas (CAPI / CAWI / Anti-Fraud / Validasi)",
    "geospatial": "Sistem Informasi Geografis & WebGIS Statistik Spasial",
    "dissemination_dashboard": "Diseminasi, Visualisasi & Semantic Portal Data Statistik",
    "other": "Tata Kelola & Sistem Pendukung Statistik Lainnya",
}

# Pre-defined strategic opportunities per cluster adhering to Polstat STIS SIS criteria
CLUSTER_STRATEGIC_OPPORTUNITIES = {
    "security_privacy": [
        "Penerapan On-Demand Microdata Query Engine dengan Differential Privacy matematis (Laplace/Gaussian mechanism) untuk rilis data mikro BPS yang patuh UU PDP No. 27/2022.",
        "Implementasi Cryptographic Audit Trail (Merkle Tree / Hash Chaining) untuk pelacakan konsumsi privacy budget (epsilon) dan pencegahan rekonstruksi basis data.",
        "Hardening & DevSecOps Automated Vulnerability Pipeline pada RESTful API mikrodata statistik guna mencegah celah OWASP API Top 10.",
    ],
    "sdi_interoperability": [
        "Rancang Bangun Secure API Gateway Satu Data Indonesia dengan Zero-Trust Architecture (NIST SP 800-207) dan mTLS untuk pertukaran data lintas K/L/D.",
        "Sistem Penilaian Kualitas dan Kesesuaian Metadata Statistik Sektoral Otomatis berbasis representasi graf/NLP untuk standardisasi SIMETRIS.",
        "Middleware interoperabilitas data spasial dan numerik berbasis standar SDMX / OGC untuk sinkronisasi data antar-OPD di portal Satu Data daerah.",
    ],
    "data_collection_capi": [
        "Backend Deteksi Anomali dan Falsifikasi Data Survei Lapangan BPS secara Real-Time menggunakan analisis paradatak (dwell-time dan sekuens entri).",
        "Enkripsi Terisolasi & Otomasi Verifikasi Integritas Data Entri pada CAPI Mobile Offline-First untuk mengamankan data sensus di ponsel mitra pencacah.",
        "Sistem Asisten Validasi Data Entri Multimodal berbasis AI/LLM pada aplikasi CAPI untuk deteksi otomatis anomali deskripsi KBLI/KBKI.",
    ],
    "geospatial": [
        "WebGIS Interaktif untuk Pemantauan dan Pemutakhiran Batas Satuan Lingkungan Setempat (SLS) Sensus dengan Sinkronisasi Spasial Offline-Online.",
        "Platform Integrasi Data Penginderaan Jauh dan Data Sensus untuk Estimasi Indikator SDGs Tingkat Kecamatan/Desa.",
    ],
    "dissemination_dashboard": [
        "Dashboard Analitik Diseminasi Statistik Terintegrasi dengan Semantic Search dan LLM RAG yang terhubung ke basis data publikasi BPS.",
        "Portal Open Data Statistik Interaktif dengan Pengendalian Pengungkapan Statistik (SDC) Otomatis dan Visualisasi Mikrodata Dinamis.",
    ],
}


class BrainstormSynthesizer:
    """Synthesizes raw gap items into structured research problem mappings and opportunities."""

    def __init__(self, gap_items: Optional[List[ResearchGapItem]] = None):
        self.gap_items = gap_items or []

    def load_items(self, items: List[ResearchGapItem]) -> None:
        """Load or replace current gap items."""
        self.gap_items = items

    def synthesize_by_cluster(self) -> Dict[str, BrainstormClusterSummary]:
        """Group gap items by cluster and synthesize problems, bottlenecks, and opportunities."""
        summaries: Dict[str, BrainstormClusterSummary] = {}

        for cluster_id, cluster_name in CLUSTER_NAMES.items():
            summaries[cluster_id] = BrainstormClusterSummary(
                cluster_id=cluster_id,
                cluster_name=cluster_name,
                open_problems=[],
                methodological_bottlenecks=[],
                future_works=[],
                synthesized_opportunities=list(CLUSTER_STRATEGIC_OPPORTUNITIES.get(cluster_id, [])),
            )

        for item in self.gap_items:
            cluster_id = item.cluster if item.cluster in summaries else "other"
            summary = summaries[cluster_id]

            if item.gap_category == "open_problem":
                summary.open_problems.append(item)
            elif item.gap_category == "methodological_bottleneck":
                summary.methodological_bottlenecks.append(item)
            elif item.gap_category == "future_work":
                summary.future_works.append(item)

        return summaries

    def generate_research_matrix(self) -> List[Dict[str, str]]:
        """Generate a comparison matrix across top clusters: Past Theses Pattern vs Gap vs Proposed Novelty."""
        matrix = [
            {
                "cluster": "Keamanan & Privasi Data Mikro",
                "past_pattern": "Masking statis offline file CSV/SAV (sdcMicro di R/Python script), fokus murni matematis disclosure risk.",
                "methodological_bottleneck": "Tidak real-time, rentan terhadap linkage & reconstruction attack, mengabaikan keamanan API dan audit budget privasi.",
                "proposed_novelty": "Secure On-Demand Query Engine dengan Differential Privacy (Laplace mechanism) dan Cryptographic Audit Trail berbasis API.",
                "stis_suitability": "Sangat Tinggi (Sesuai UU PDP No. 27/2022 & DSRM rekayasa backend, feasible 6 bulan).",
            },
            {
                "cluster": "Interoperabilitas & Satu Data Indonesia",
                "past_pattern": "Portal Satu Data lokal CRUD standar (Laravel/Django) dengan REST API token statis sederhana.",
                "methodological_bottleneck": "Tanpa enkripsi payload antar-OPD, validasi metadata SIMETRIS masih manual, rentan terhadap MITM dan API abuse.",
                "proposed_novelty": "API Gateway Satu Data berbasis Zero-Trust Architecture (mTLS, rate limiting, token rotation) + Otomasi Validasi Kualitas Metadata.",
                "stis_suitability": "Sangat Tinggi (Sesuai Perpres 39/2019 SDI & SPBE, pengujian ISO/IEC 25010).",
            },
            {
                "cluster": "Pengumpulan Data / CAPI Cerdas",
                "past_pattern": "Aplikasi CAPI mobile/web dengan validasi logika hardcoded dasar (skip pattern, range check).",
                "methodological_bottleneck": "Tidak ada deteksi falsifikasi lapangan/curbstoning; penyimpanan data lokal di ponsel mitra belum terenkripsi.",
                "proposed_novelty": "Backend Deteksi Anomali & Falsifikasi Pencacahan berbasis Paradatak Waktu (Dwell-Time) & Secure Local Storage CAPI.",
                "stis_suitability": "Sangat Tinggi (Mengatasi isu riil kualitas survei BPS, integrasi GSBPM Tahap 4 Collect).",
            },
        ]
        return matrix
