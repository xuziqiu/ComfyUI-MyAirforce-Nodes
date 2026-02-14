# Airforce ComfyUI node pack: register nodes from submodules

from .config import AirforceConfig
from .upload import AirforceAnonDropUpload
from .params import (
    AirforceNanoParams,
    AirforceFluxProFlexParams,
    AirforceFluxDevKleinParams,
    AirforceZImageParams,
    AirforceImagenParams,
    AirforceSeedreamParams,
    AirforceSunoParams,
    AirforceGrokImagineVideoParams,
    AirforceVeoParams,
    AirforceWanParams,
)
from .generator import AirforceGeneratorModular, AirforceVideoGeneratorModular

NODE_CLASS_MAPPINGS = {
    "AirforceConfig": AirforceConfig,
    "AirforceAnonDropUpload": AirforceAnonDropUpload,
    "AirforceNanoParams": AirforceNanoParams,
    "AirforceFluxProFlexParams": AirforceFluxProFlexParams,
    "AirforceFluxDevKleinParams": AirforceFluxDevKleinParams,
    "AirforceZImageParams": AirforceZImageParams,
    "AirforceImagenParams": AirforceImagenParams,
    "AirforceSeedreamParams": AirforceSeedreamParams,
    "AirforceSunoParams": AirforceSunoParams,
    "AirforceGrokImagineVideoParams": AirforceGrokImagineVideoParams,
    "AirforceVeoParams": AirforceVeoParams,
    "AirforceWanParams": AirforceWanParams,
    "AirforceGeneratorModular": AirforceGeneratorModular,
    "AirforceVideoGeneratorModular": AirforceVideoGeneratorModular,
}

# Icons: config, params, submit, upload. (Image)/(Video) in parentheses. Submit uses different icon from suite.
NODE_DISPLAY_NAME_MAPPINGS = {
    "AirforceConfig": "⚙️ Airforce: Config",
    "AirforceAnonDropUpload": "📤 Reference: AnonDrop Upload",
    "AirforceNanoParams": "📝 NanoBanana (Image)",
    "AirforceFluxProFlexParams": "📝 Flux Pro/Flex (Image)",
    "AirforceFluxDevKleinParams": "📝 Flux Dev/Klein (Image)",
    "AirforceZImageParams": "📝 Z-Image (Image)",
    "AirforceImagenParams": "📝 Imagen (Image)",
    "AirforceSeedreamParams": "📝 Seedream (Image)",
    "AirforceSunoParams": "📝 Suno (Video)",
    "AirforceGrokImagineVideoParams": "📝 Grok Imagine (Video)",
    "AirforceVeoParams": "📝 Veo (Video)",
    "AirforceWanParams": "📝 Wan (Video)",
    "AirforceGeneratorModular": "🎨 Airforce: Submit (Image)",
    "AirforceVideoGeneratorModular": "🎬 Airforce: Submit (Video)",
}

__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
]
