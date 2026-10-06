"""
calm_carson.style
Sub-paket audit dan evaluasi gaya penulisan AI (Signs of AI Writing) untuk naskah akademik.
Mengadopsi panduan Wikipedia:Signs_of_AI_writing, PUEBI/EYD V, dan standar sitasi IEEE.
"""

from calm_carson.style.checker import (
    AIStyleChecker,
    check_file_style,
    check_text_style,
)
from calm_carson.style.exporter import StyleExporter
from calm_carson.style.models import (
    StyleMetrics,
    StyleReport,
    StyleSeverity,
    StyleViolation,
    StyleViolationType,
)

__all__ = [
    "AIStyleChecker",
    "StyleReport",
    "StyleViolation",
    "StyleViolationType",
    "StyleSeverity",
    "StyleMetrics",
    "StyleExporter",
    "check_text_style",
    "check_file_style",
]
