"""
Data models for AI Writing Style Checker.
Mendefinisikan tipe pelanggaran, tingkat keparahan, metrik teks, dan laporan audit gaya penulisan AI.
Berdasarkan taksonomi Wikipedia:Signs_of_AI_writing (WikiProject AI Cleanup).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class StyleViolationType(str, Enum):
    """Kategori pelanggaran gaya penulisan AI berdasarkan panduan Wikipedia."""
    CHATBOT_LEAK = "CHATBOT_LEAK"                      # Token internal LLM (oaicite, turn0search0, cite, grok, etc.)
    CONVERSATIONAL_FILLER = "CONVERSATIONAL_FILLER"    # Sapaan / respons obrolan ("Certainly!", "I hope this helps", dll.)
    KNOWLEDGE_CUTOFF = "KNOWLEDGE_CUTOFF"              # Penafian batas pengetahuan ("As of my last update", dll.)
    AI_VOCABULARY = "AI_VOCABULARY"                    # Kosakata klise AI (delve, tapestry, pivotal, menyelami, dll.)
    COPULATIVE_AVOIDANCE = "COPULATIVE_AVOIDANCE"      # Penghindaran 'adalah/is' -> serves as a, berperan sebagai
    VAGUE_ASSOCIATION = "VAGUE_ASSOCIATION"            # Hubungan samar ("associated with", "terkait dengan")
    NEGATIVE_PARALLELISM = "NEGATIVE_PARALLELISM"      # "Not just X, but also Y", "Tidak hanya X, tetapi juga Y"
    RULE_OF_THREE = "RULE_OF_THREE"                    # Trio kata sifat/frasa formulaik berulang
    SUPERFICIAL_ANALYSIS = "SUPERFICIAL_ANALYSIS"      # Buntut partisipel -ing / klausa penutup tanpa data riil
    FORMULAIC_CONCLUSION = "FORMULAIC_CONCLUSION"      # "Despite these challenges...", "Menatap masa depan..."
    INLINE_HEADER_LIST = "INLINE_HEADER_LIST"          # Dominasi daftar ber-bullet tajuk tebal alih-alih paragraf
    EM_DASH_OVERUSE = "EM_DASH_OVERUSE"                # Penggunaan em dash (—) berlebih / tidak sesuai kaidah PUEBI/MOS
    CURLY_QUOTES = "CURLY_QUOTES"                      # Tanda petik lengkung khas salinan chatbot
    BURSTINESS_LOW = "BURSTINESS_LOW"                  # Ritme kalimat monoton / variansi panjang kalimat rendah


class StyleSeverity(str, Enum):
    """Tingkat keparahan pelanggaran gaya penulisan."""
    FATAL = "FATAL"      # Kebocoran token sistem, penafian cutoff, sapaan chatbot (Wajib ditolak)
    HIGH = "HIGH"        # Kesimpulan formulaik, kepadatan klise AI tinggi, analisis semu gerund
    MEDIUM = "MEDIUM"    # Penghindaran copula, negative parallelism, em-dash berlebih, daftar berlebih
    LOW = "LOW"          # Rule-of-three terisolasi, gaya minor
    INFO = "INFO"        # Informasi statistik dan saran variasi gaya


@dataclass
class StyleViolation:
    """Detail satu temuan anomali gaya penulisan."""
    violation_type: StyleViolationType
    severity: StyleSeverity
    rule_name: str
    matched_text: str
    line_number: int
    sentence: str
    explanation: str
    suggested_fix: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "violation_type": self.violation_type.value,
            "severity": self.severity.value,
            "rule_name": self.rule_name,
            "matched_text": self.matched_text,
            "line_number": self.line_number,
            "sentence": self.sentence,
            "explanation": self.explanation,
            "suggested_fix": self.suggested_fix,
        }


@dataclass
class StyleMetrics:
    """Metrik kuantitatif struktur dan gaya bahasa draf teks."""
    total_words: int = 0
    total_sentences: int = 0
    total_paragraphs: int = 0
    avg_sentence_length: float = 0.0
    sentence_length_std_dev: float = 0.0
    burstiness_score: float = 0.0  # std_dev / avg (semakin rendah, semakin monoton/robotik)
    bullet_line_ratio: float = 0.0
    em_dash_count: int = 0
    vocabulary_richness: float = 0.0  # Type-Token Ratio (TTR)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_words": self.total_words,
            "total_sentences": self.total_sentences,
            "total_paragraphs": self.total_paragraphs,
            "avg_sentence_length": round(self.avg_sentence_length, 2),
            "sentence_length_std_dev": round(self.sentence_length_std_dev, 2),
            "burstiness_score": round(self.burstiness_score, 3),
            "bullet_line_ratio": round(self.bullet_line_ratio, 3),
            "em_dash_count": self.em_dash_count,
            "vocabulary_richness": round(self.vocabulary_richness, 3),
        }


@dataclass
class StyleReport:
    """Laporan komprehensif hasil evaluasi gaya penulisan AI."""
    source_identifier: str
    ai_risk_score: int  # Skor risiko 0 - 100
    risk_verdict: str   # CLEAN_ACADEMIC, LOW_RISK, SUSPICIOUS_AI_PATTERNS, HIGH_RISK_AI_GENERATED
    total_violations: int
    fatal_count: int
    high_count: int
    medium_count: int
    low_count: int
    violations: List[StyleViolation] = field(default_factory=list)
    metrics: StyleMetrics = field(default_factory=StyleMetrics)
    annotated_text: str = ""
    summary_verdict: str = ""

    def is_acceptable(self, strict: bool = False) -> bool:
        """Menentukan apakah draf dapat diterima untuk penulisan akademik."""
        if self.fatal_count > 0:
            return False
        if strict and (self.high_count > 0 or self.ai_risk_score >= 35):
            return False
        return self.ai_risk_score < 50

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_identifier": self.source_identifier,
            "ai_risk_score": self.ai_risk_score,
            "risk_verdict": self.risk_verdict,
            "summary_verdict": self.summary_verdict,
            "total_violations": self.total_violations,
            "counts": {
                "fatal": self.fatal_count,
                "high": self.high_count,
                "medium": self.medium_count,
                "low": self.low_count,
            },
            "metrics": self.metrics.to_dict(),
            "violations": [v.to_dict() for v in self.violations],
        }
