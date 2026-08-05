from typing import Dict, Any, Optional
from vorik_schemas.models import ImageGenerationRequest, MediaJobResponse

INDIAN_CONTEXT_PRESETS = {
    "Kerala": "traditional Kerala architecture, lush green coconut palms, soft golden hour lighting, cinematic film quality",
    "North India": "rich warm hues, authentic brick architecture, vibrant textiles, natural ambient sunlight",
    "Tamil Nadu": "classic Dravidian temple backdrop, warm tropical sunlight, crisp high-resolution photography",
    "Urban Tech Hub": "modern glass office interior, sleek contemporary lighting, professional corporate setting",
}

DEFAULT_NEGATIVE_PROMPT = (
    "blurry, distorted face, extra limbs, cartoonish, low resolution, bad anatomy, "
    "stereotypical caricature, oversaturated, unnatural skin tone"
)

class ImageGenerationEngine:
    """Self-hosted image generation prompt synthesis and GPU job dispatcher"""

    def build_prompt(self, req: ImageGenerationRequest, character_modifier: str = "") -> Dict[str, str]:
        context_preset = INDIAN_CONTEXT_PRESETS.get(req.region_context, "authentic Indian environmental setting, professional lighting")
        
        full_prompt = f"{req.prompt}. {character_modifier} {context_preset}, highly detailed 8k photography, 35mm lens."
        negative_prompt = f"{req.negative_prompt}, {DEFAULT_NEGATIVE_PROMPT}" if req.negative_prompt else DEFAULT_NEGATIVE_PROMPT

        return {
            "prompt": full_prompt,
            "negative_prompt": negative_prompt,
            "aspect_ratio": req.aspect_ratio,
            "width": req.width,
            "height": req.height
        }
