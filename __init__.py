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
from .generator import AirforceGeneratorModular
from .download import AirforceDownload
from .preview import AirforceVideoPreview

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
    "AirforceDownload": AirforceDownload,
    "AirforceVideoPreview": AirforceVideoPreview,
}

# Params: 🎨 = image, 🎬 = video. Submit is generic (image/video depends on connected params).
NODE_DISPLAY_NAME_MAPPINGS = {
    "AirforceConfig": "⚙️ Airforce: Config",
    "AirforceAnonDropUpload": "📤 Reference: AnonDrop Upload",
    "AirforceNanoParams": "🎨 NanoBanana",
    "AirforceFluxProFlexParams": "🎨 Flux Pro/Flex",
    "AirforceFluxDevKleinParams": "🎨 Flux Dev/Klein",
    "AirforceZImageParams": "🎨 Z-Image",
    "AirforceImagenParams": "🎨 Imagen",
    "AirforceSeedreamParams": "🎨 Seedream",
    "AirforceSunoParams": "🎬 Suno",
    "AirforceGrokImagineVideoParams": "🎬 Grok Imagine",
    "AirforceVeoParams": "🎬 Veo",
    "AirforceWanParams": "🎬 Wan",
    "AirforceGeneratorModular": "🎯 Airforce: Submit",
    "AirforceDownload": "⬇️ Airforce: Download",
    "AirforceVideoPreview": "📺 Airforce Previewer",
}

WEB_DIRECTORY = "./web"

__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
    "WEB_DIRECTORY",
]
