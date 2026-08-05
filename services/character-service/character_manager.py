from typing import Dict, Any, List, Optional
from vorik_schemas.models import CharacterProfile

DEFAULT_CHARACTERS = {
    "char_meera_01": CharacterProfile(
        character_id="char_meera_01",
        name="Meera",
        region="Kerala",
        age_range="35-40",
        skin_tone="medium brown",
        face_description="oval face with natural expressions and dark brown eyes",
        hair="black shoulder-length lightly wavy hair",
        wardrobe="contemporary Kerala handloom sarees and elegant linen wear",
        voice_language="Malayalam",
        accent="Central Kerala",
        personality="warm, composed, and professional",
        consent_status="synthetic"
    ),
    "char_arjun_02": CharacterProfile(
        character_id="char_arjun_02",
        name="Arjun",
        region="Telangana",
        age_range="28-32",
        skin_tone="tan brown",
        face_description="sharp jawline, short trimmed beard, confident smile",
        hair="short dark cropped hair",
        wardrobe="modern smart-casual shirts and blazer",
        voice_language="Telugu",
        accent="Hyderabad urban",
        personality="dynamic, tech-savvy, and articulated",
        consent_status="synthetic"
    )
}

class CharacterManager:
    """Reusable Character Consistency profile manager"""

    def __init__(self):
        self.profiles: Dict[str, CharacterProfile] = DEFAULT_CHARACTERS.copy()

    def get_character(self, character_id: str) -> Optional[CharacterProfile]:
        return self.profiles.get(character_id)

    def create_character(self, profile: CharacterProfile) -> CharacterProfile:
        self.profiles[profile.character_id] = profile
        return profile

    def build_character_prompt_modifier(self, character_id: str) -> str:
        char = self.get_character(character_id)
        if not char:
            return ""
        return (
            f"Consistent character {char.name} from {char.region}, age {char.age_range}, "
            f"{char.skin_tone} skin tone, {char.face_description}, wearing {char.wardrobe}."
        )
