import re
from typing import Dict, Any, List
from vorik_schemas.models import LanguageEnum, ScriptEnum, LanguageDetectionResult

SCRIPT_RANGES = {
    ScriptEnum.DEVANAGARI: (0x0900, 0x097F),
    ScriptEnum.BENGALI: (0x0980, 0x09FF),
    ScriptEnum.GURMUKHI: (0x0A00, 0x0A7F),
    ScriptEnum.GUJARATI: (0x0A80, 0x0AFF),
    ScriptEnum.ODIA: (0x0B00, 0x0B7F),
    ScriptEnum.TAMIL: (0x0B80, 0x0BFF),
    ScriptEnum.TELUGU: (0x0C00, 0x0C7F),
    ScriptEnum.KANNADA: (0x0C80, 0x0CFF),
    ScriptEnum.MALAYALAM: (0x0D00, 0x0D7F),
    ScriptEnum.ARABIC: (0x0600, 0x06FF),
}

ROMANISED_MARKERS = {
    LanguageEnum.HINDI: ["kya", "kar", "rha", "hai", "bhai", "namaste", "chahiye", "kuch", "apne", "bahut"],
    LanguageEnum.MALAYALAM: ["enikku", "cheyyan", "undu", "nalla", "poya", "varumo", "ayirunnu", "nokku"],
    LanguageEnum.TAMIL: ["vanakkam", "epdi", "irukinga", "theriyum", "pannanum", "nalla", "sollo"],
    LanguageEnum.TELUGU: ["ela", "unnavu", "cheyali", "bavunnara", "kavali", "nenu", "kuda"],
    LanguageEnum.KANNADA: ["hegidira", "madi", "beku", "namaskara", "yelli", "houdu"],
}

TRANSLITERATION_MAP = {
    "namaste": "नमस्ते",
    "kya kar rha hai": "क्या कर रहा है",
    "enikku help venam": "എനിക്ക് ഹെൽപ്പ് വേണം",
    "vanakkam epdi irukinga": "வணக்கம் எப்படி இருக்கீங்க",
}

class IndicLanguageEngine:
    """India-first language detection, script analysis, and code-mixed transliteration engine"""

    def detect(self, text: str) -> LanguageDetectionResult:
        # Check native scripts
        for script, (start, end) in SCRIPT_RANGES.items():
            if any(start <= ord(char) <= end for char in text):
                lang = self._script_to_language(script)
                return LanguageDetectionResult(
                    detected_language=lang,
                    detected_script=script,
                    is_romanised=False,
                    is_code_mixed=False,
                    confidence_score=0.98
                )

        # Check Romanised / Code-Mixed Indic text
        lower_text = text.lower()
        words = re.findall(r'\w+', lower_text)

        for lang, markers in ROMANISED_MARKERS.items():
            matched_markers = [w for w in words if w in markers]
            if matched_markers:
                return LanguageDetectionResult(
                    detected_language=lang,
                    detected_script=ScriptEnum.LATIN,
                    is_romanised=True,
                    is_code_mixed=True,
                    confidence_score=min(0.70 + 0.1 * len(matched_markers), 0.96),
                    secondary_languages=["english"]
                )

        # Default fallback to English
        return LanguageDetectionResult(
            detected_language=LanguageEnum.ENGLISH,
            detected_script=ScriptEnum.LATIN,
            is_romanised=False,
            is_code_mixed=False,
            confidence_score=0.90
        )

    def _script_to_language(self, script: ScriptEnum) -> LanguageEnum:
        mapping = {
            ScriptEnum.DEVANAGARI: LanguageEnum.HINDI,
            ScriptEnum.MALAYALAM: LanguageEnum.MALAYALAM,
            ScriptEnum.TAMIL: LanguageEnum.TAMIL,
            ScriptEnum.TELUGU: LanguageEnum.TELUGU,
            ScriptEnum.KANNADA: LanguageEnum.KANNADA,
            ScriptEnum.BENGALI: LanguageEnum.BENGALI,
            ScriptEnum.GUJARATI: LanguageEnum.GUJARATI,
            ScriptEnum.GURMUKHI: LanguageEnum.PUNJABI,
            ScriptEnum.ARABIC: LanguageEnum.URDU,
            ScriptEnum.ODIA: LanguageEnum.ODIA,
        }
        return mapping.get(script, LanguageEnum.HINDI)

    def transliterate(self, text: str) -> str:
        lower_text = text.lower().strip()
        return TRANSLITERATION_MAP.get(lower_text, text)
