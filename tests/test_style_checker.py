"""
Unit tests for AI Writing Style Checker (calm_carson.style).
Menguji pendeteksian kebocoran token LLM, sapaan percakapan, klise kosakata dwibahasa,
pelanggaran tanda pisah (em dash PUEBI), kesimpulan formulaik, metrik burstiness, serta CLI runner.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from calm_carson.style import (
    AIStyleChecker,
    StyleExporter,
    StyleSeverity,
    StyleViolationType,
    check_file_style,
    check_text_style,
)


class TestAIStyleChecker(unittest.TestCase):
    """Test suite untuk modul audit gaya penulisan AI."""

    def setUp(self) -> None:
        self.checker = AIStyleChecker()

    def test_chatbot_leaks_fatal(self) -> None:
        """Menguji deteksi token internal chatbot (ChatGPT, Gemini, DeepSeek)."""
        leak_text = (
            "Klasifikasi sensus diperbarui :contentReference[oaicite:14]{index=14} "
            "berdasarkan data BPS. Pengujian model [cite: 3] menghasilkan akurasi 94% "
            "dan rujukan DeepSeek 【2†source】 menunjukkan persistensi data."
        )
        report = self.checker.check_text(leak_text)

        self.assertGreaterEqual(report.fatal_count, 3)
        self.assertGreaterEqual(report.ai_risk_score, 75)
        self.assertEqual(report.risk_verdict, "HIGH_RISK_AI_GENERATED")

        leak_types = [v.violation_type for v in report.violations]
        self.assertIn(StyleViolationType.CHATBOT_LEAK, leak_types)

    def test_conversational_filler_and_cutoffs(self) -> None:
        """Menguji deteksi sapaan korespondensi AI dan penafian batas pengetahuan."""
        text = (
            "Tentu saja! Berikut adalah draf latar belakang penelitian yang Anda minta.\n"
            "Certainly! Here is a breakdown of the statistical framework.\n"
            "Hingga batas pembaruan pengetahuan saya, data sensus belum dipublikasikan secara terbuka."
        )
        report = self.checker.check_text(text)

        self.assertGreaterEqual(report.fatal_count, 3)
        rule_names = [v.rule_name for v in report.violations]
        self.assertIn("conversational_salutation_id", rule_names)
        self.assertIn("conversational_salutation_en", rule_names)
        self.assertIn("knowledge_cutoff_id", rule_names)

    def test_em_dash_violations_puebi(self) -> None:
        """
        Menguji deteksi tanda pisah (em dash '—') berspasi (melanggar PUEBI/EYD V)
        dan kepadatan em dash yang berlebihan.
        """
        # 1. Tanda pisah berspasi khas AI
        spaced_text = "Aplikasi CAPI — yang dibangun menggunakan Flutter — diuji di 34 provinsi."
        report = self.checker.check_text(spaced_text)

        em_dash_violations = [
            v for v in report.violations if v.violation_type == StyleViolationType.EM_DASH_OVERUSE
        ]
        self.assertGreaterEqual(len(em_dash_violations), 1)
        self.assertEqual(em_dash_violations[0].rule_name, "spaced_em_dash_typography")

        # 2. Tanda pisah ganda / berulang dalam satu kalimat (dramatisasi)
        multi_em_dash = "Sistem ini—yang diuji kemarin—menunjukkan peningkatan—secara dramatis."
        report_multi = self.checker.check_text(multi_em_dash)
        density_violations = [
            v for v in report_multi.violations if v.rule_name == "excessive_em_dash_density"
        ]
        self.assertGreaterEqual(len(density_violations), 1)

    def test_ai_vocabulary_id_and_en(self) -> None:
        """Menguji pendeteksian kosakata klise AI dwibahasa (Indonesia & Inggris)."""
        text_id = (
            "Di era modern ini, tidak dapat dipungkiri bahwa pengumpulan data "
            "memainkan peran krusial dalam lanskap yang dinamis, menjadi bukti nyata kemajuan."
        )
        report_id = self.checker.check_text(text_id)

        vocab_rules_id = [v.rule_name for v in report_id.violations]
        self.assertIn("id_era_modern", vocab_rules_id)
        self.assertIn("id_tidak_dapat_dipungkiri", vocab_rules_id)
        self.assertIn("id_peran_krusial", vocab_rules_id)
        self.assertIn("id_lanskap_dinamis", vocab_rules_id)
        self.assertIn("id_bukti_nyata", vocab_rules_id)

        text_en = (
            "We delve into the intricate interplay of components within this dynamic landscape, "
            "which underscores the pivotal importance of secure data dissemination."
        )
        report_en = self.checker.check_text(text_en)
        vocab_rules_en = [v.rule_name for v in report_en.violations]
        self.assertIn("delve_into", vocab_rules_en)
        self.assertIn("intricate_interplay", vocab_rules_en)
        self.assertIn("dynamic_landscape", vocab_rules_en)
        self.assertIn("pivotal_role", vocab_rules_en)

    def test_copulative_avoidance_and_negative_parallelisms(self) -> None:
        """Menguji deteksi copulative avoidance dan negative parallelisms."""
        text = (
            "The proposed gateway serves as a foundation for national interoperability. "
            "Not only does it improve data transmission speed, but also it reduces error rates. "
            "Sistem ini tidak hanya memvalidasi data GPS, tetapi juga memvalidasi timestamp entri."
        )
        report = self.checker.check_text(text)

        types = [v.violation_type for v in report.violations]
        self.assertIn(StyleViolationType.COPULATIVE_AVOIDANCE, types)
        self.assertIn(StyleViolationType.NEGATIVE_PARALLELISM, types)

    def test_superficial_analysis_and_formulaic_conclusions(self) -> None:
        """Menguji deteksi buntut partisipel pemanis dan kesimpulan outline formulaik."""
        text = (
            "Integrasi SQLite selesai dilakukan pada kuartal ketiga, sehingga menegaskan pentingnya data mikro.\n"
            "Meskipun menghadapi berbagai tantangan, arsitektur Satu Data Indonesia tetap memiliki prospek cerah.\n"
            "Despite these challenges, the system faces several obstacles in implementation."
        )
        report = self.checker.check_text(text)

        types = [v.violation_type for v in report.violations]
        self.assertIn(StyleViolationType.SUPERFICIAL_ANALYSIS, types)
        self.assertIn(StyleViolationType.FORMULAIC_CONCLUSION, types)

    def test_rule_of_three_detection(self) -> None:
        """Menguji deteksi pola ritmis rule of three berulang."""
        text = "Sistem yang dikembangkan harus efisien, andal, dan terukur dalam memproses data."
        report = self.checker.check_text(text)

        types = [v.violation_type for v in report.violations]
        self.assertIn(StyleViolationType.RULE_OF_THREE, types)

    def test_clean_academic_text(self) -> None:
        """Menguji bahwa naskah akademik yang objektif dan berbasis angka dinyatakan lolos (CLEAN)."""
        clean_text = (
            "Berdasarkan hasil evaluasi Sensus Pertanian 2023, sistem validasi CAPI berhasil "
            "menurunkan tingkat galat entri data sebesar 23,4% dibandingkan metode PAPI [1]. "
            "Pengujian fungsionalitas menggunakan standar ISO/IEC 25010 menunjukkan nilai kesesuaian 91,2% [2]. "
            "Proses sinkronisasi data mikro dilakukan melalui protokol HTTPS terenkripsi TLS 1.3 "
            "dengan latensi rata-rata 120 milidetik pada jaringan 4G."
        )
        report = self.checker.check_text(clean_text)

        self.assertLess(report.ai_risk_score, 20)
        self.assertEqual(report.risk_verdict, "CLEAN_ACADEMIC")
        self.assertTrue(report.is_acceptable(strict=True))
        self.assertEqual(report.fatal_count, 0)
        self.assertEqual(report.high_count, 0)

    def test_exporter_markdown_and_json(self) -> None:
        """Menguji rendering terminal dan ekspor berkas Markdown serta JSON."""
        text = "Di era modern ini, sistem ini memainkan peran penting — membuktikan komitmen BPS."
        report = self.checker.check_text(text, source_id="test_export")

        # Terminal render
        terminal_out = StyleExporter.render_terminal(report, show_annotated=True)
        self.assertIn("CALM-CARSON: AUDIT GAYA PENULISAN AI", terminal_out)
        self.assertIn("Indeks Risiko AI", terminal_out)

        # Markdown export
        with tempfile.TemporaryDirectory() as tmpdir:
            md_path = Path(tmpdir) / "report.md"
            json_path = Path(tmpdir) / "report.json"

            StyleExporter.export_markdown(report, md_path)
            StyleExporter.export_json(report, json_path)

            self.assertTrue(md_path.exists())
            self.assertTrue(json_path.exists())

            # Validasi isi JSON
            data = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertEqual(data["source_identifier"], "test_export")
            self.assertIn("violations", data)
            self.assertIn("metrics", data)

    def test_cli_runner_execution(self) -> None:
        """Menguji eksekusi CLI scripts/check_ai_style.py."""
        script_path = Path(__file__).resolve().parent.parent / "scripts" / "check_ai_style.py"

        # 1. Clean text via CLI
        clean_text = "Implementasi algoritma AES-256 pada basis data SQLite berhasil menahan serangan kebocoran data [1]."
        res_clean = subprocess.run(
            [sys.executable, str(script_path), "--text", clean_text, "--strict"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(res_clean.returncode, 0, f"Clean text failed: {res_clean.stderr}")

        # 2. Heavy AI text with strict flag -> should exit with code 1
        ai_text = (
            "Certainly! Di era modern ini, tidak dapat dipungkiri bahwa :contentReference[oaicite:1] "
            "memainkan peran krusial dalam lanskap yang dinamis — membuktikan eksistensi BPS."
        )
        res_ai = subprocess.run(
            [sys.executable, str(script_path), "--text", ai_text, "--strict"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(res_ai.returncode, 1, "Strict mode should exit with code 1 for fatal AI text.")


if __name__ == "__main__":
    unittest.main()
