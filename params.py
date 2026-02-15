from .config import MODEL_REGISTRY, ASPECT_RATIO_PRESETS
from .upload import parse_image_urls


def _flux_dim(v):
    """Flux width/height: 256-2048, must be multiple of 8."""
    v = max(256, min(2048, int(v)))
    return (v // 8) * 8


class AirforceNanoParams:
    @classmethod
    def INPUT_TYPES(cls):
        nano_models = MODEL_REGISTRY["nano"]["models"]
        return {
            "required": {
                "model": (nano_models, {"default": nano_models[0]}),
                "aspectRatio": (ASPECT_RATIO_PRESETS, {"default": "1:1"}),
                "resolution": (["1k", "2k", "4k"], {"default": "1k"}),
            },
            "optional": {
                "reference_urls": ("STRING", {"default": "", "placeholder": "From AnonDrop Upload node, one URL per line, max 8"}),
            }
        }

    RETURN_TYPES = ("AF_PARAMS",)
    RETURN_NAMES = ("params",)
    FUNCTION = "pack"
    CATEGORY = "🚀Airforce/Modular"

    def pack(self, model, aspectRatio, resolution, reference_urls=None):
        payload = {
            "model": model,
            "n": 1,
            "size": "1024x1024",
            "response_format": "url",
            "aspectRatio": aspectRatio,
            "resolution": resolution
        }
        urls = parse_image_urls(reference_urls, max_count=8)
        if urls is not None:
            payload["image_urls"] = urls
        return ({"payload": payload, },)


FLUX_PRO_FLEX_MODELS = ["flux-2-pro", "flux-2-flex"]
FLUX_DEV_KLEIN_MODELS = ["flux-2-dev", "flux-2-klein-9b", "flux-2-klein-4b"]


class AirforceFluxProFlexParams:
    """Flux Pro / Flex: aspectRatio + resolution (1k/2k), reference images max 8."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": (FLUX_PRO_FLEX_MODELS, {"default": FLUX_PRO_FLEX_MODELS[0]}),
                "aspectRatio": (ASPECT_RATIO_PRESETS, {"default": "1:1"}),
                "resolution": (["1k", "2k"], {"default": "1k"}),
            },
            "optional": {
                "reference_urls": ("STRING", {"default": "", "placeholder": "From AnonDrop Upload, one URL per line, max 8"}),
            }
        }

    RETURN_TYPES = ("AF_PARAMS",)
    RETURN_NAMES = ("params",)
    FUNCTION = "pack"
    CATEGORY = "🚀Airforce/Modular"

    def pack(self, model, aspectRatio, resolution, reference_urls=None):
        payload = {
            "model": model,
            "n": 1,
            "size": "1024x1024",
            "response_format": "url",
            "aspectRatio": aspectRatio,
            "resolution": resolution,
        }
        urls = parse_image_urls(reference_urls, max_count=8)
        if urls is not None:
            payload["image_urls"] = urls
        return ({"payload": payload, },)


class AirforceFluxDevKleinParams:
    """Flux Dev / Klein: width and height in pixels, reference images max 4."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": (FLUX_DEV_KLEIN_MODELS, {"default": FLUX_DEV_KLEIN_MODELS[0]}),
                "width": ("INT", {"default": 1024, "min": 256, "max": 2048, "step": 8}),
                "height": ("INT", {"default": 1024, "min": 256, "max": 2048, "step": 8}),
            },
            "optional": {
                "reference_urls": ("STRING", {"default": "", "placeholder": "From AnonDrop Upload, one URL per line, max 4"}),
            }
        }

    RETURN_TYPES = ("AF_PARAMS",)
    RETURN_NAMES = ("params",)
    FUNCTION = "pack"
    CATEGORY = "🚀Airforce/Modular"

    def pack(self, model, width, height, reference_urls=None):
        w, h = _flux_dim(width), _flux_dim(height)
        payload = {
            "model": model,
            "n": 1,
            "size": "1024x1024",
            "response_format": "url",
            "aspectRatio": f"{w}:{h}",
        }
        urls = parse_image_urls(reference_urls, max_count=4)
        if urls is not None:
            payload["image_urls"] = urls
        return ({"payload": payload, },)


class AirforceZImageParams:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": (["z-image"], {"default": "z-image"}),
                "aspectRatio": (ASPECT_RATIO_PRESETS, {"default": "16:9"}),
            }
        }

    RETURN_TYPES = ("AF_PARAMS",)
    RETURN_NAMES = ("params",)
    FUNCTION = "pack"
    CATEGORY = "🚀Airforce/Modular"

    def pack(self, model, aspectRatio):
        return ({"payload": {
            "model": model,
            "n": 1,
            "size": "1024x1024",
            "response_format": "url",
            "aspectRatio": aspectRatio,
        }, },)


class AirforceImagenParams:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": (["imagen-3", "imagen-4"], {"default": "imagen-4"}),
            }
        }

    RETURN_TYPES = ("AF_PARAMS",)
    RETURN_NAMES = ("params",)
    FUNCTION = "pack"
    CATEGORY = "🚀Airforce/Modular"

    def pack(self, model):
        return ({"payload": {
            "model": model,
            "n": 1,
            "size": "1024x1024",
            "response_format": "url",
        }, },)


class AirforceSeedreamParams:
    """Seedream image params; reference images max 14."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": (["seedream-4.5"], {"default": "seedream-4.5"}),
                "aspectRatio": (ASPECT_RATIO_PRESETS, {"default": "1:1"}),
                "quality": (["high", "basic"], {"default": "high"}),
            },
            "optional": {
                "reference_urls": ("STRING", {"default": "", "placeholder": "From AnonDrop Upload, one URL per line, max 14"}),
            }
        }

    RETURN_TYPES = ("AF_PARAMS",)
    RETURN_NAMES = ("params",)
    FUNCTION = "pack"
    CATEGORY = "🚀Airforce/Modular"

    def pack(self, model, aspectRatio, quality, reference_urls=None):
        payload = {
            "model": model,
            "n": 1,
            "size": "1024x1024",
            "response_format": "url",
            "aspectRatio": aspectRatio,
            "quality": quality,
        }
        urls = parse_image_urls(reference_urls, max_count=14)
        if urls is not None:
            payload["image_urls"] = urls
        return ({"payload": payload, },)


class AirforceSunoParams:
    """Suno video params; style is used when custom mode is on. Order: model, instrumental, custom mode, style."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": (["suno-v5", "suno-4.5"], {"default": "suno-v5"}),
                "instrumental": ("BOOLEAN", {"default": True, "label_on": "Instrumental", "label_off": "With vocals"}),
                "custom_mode": ("BOOLEAN", {"default": True, "label_on": "On", "label_off": "Off"}),
                "style": ("STRING", {"default": "", "placeholder": "Style (used when custom mode is on)"}),
            }
        }

    RETURN_TYPES = ("AF_PARAMS",)
    RETURN_NAMES = ("params",)
    FUNCTION = "pack"
    CATEGORY = "🚀Airforce/Modular"

    def pack(self, model, instrumental, custom_mode, style):
        payload = {
            "model": model,
            "n": 1,
            "size": "1024x1024",
            "response_format": "url",
            "custom": custom_mode,
            "instrumental": instrumental,
        }
        if custom_mode:
            payload["style"] = (style or "").strip() or "default"
        return ({"payload": payload, },)


# Grok Imagine Video supports 1:1, 2:3, 3:2 only
GROK_ASPECT_RATIOS = ["1:1", "2:3", "3:2"]


class AirforceGrokImagineVideoParams:
    """Grok Imagine Video params; aspect 1:1/2:3/3:2 only; up to 2 reference images."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": (["grok-imagine-video"], {"default": "grok-imagine-video"}),
                "aspectRatio": (GROK_ASPECT_RATIOS, {"default": "2:3"}),
                "mode": (["normal", "spicy", "fun"], {"default": "spicy"}),
            },
            "optional": {
                "reference_urls": ("STRING", {"default": "", "placeholder": "From AnonDrop Upload, one URL per line, max 2"}),
            }
        }

    RETURN_TYPES = ("AF_PARAMS",)
    RETURN_NAMES = ("params",)
    FUNCTION = "pack"
    CATEGORY = "🚀Airforce/Modular"

    def pack(self, model, aspectRatio, mode, reference_urls=None):
        payload = {
            "model": model,
            "n": 1,
            "size": "1024x1024",
            "response_format": "url",
            "mode": mode,
            "aspectRatio": aspectRatio,
        }
        urls = parse_image_urls(reference_urls, max_count=2)
        if urls is not None:
            payload["image_urls"] = urls
        return ({"payload": payload, },)


class AirforceVeoParams:
    """Veo video params; prompt only, no other controls or reference images."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": (["veo-3.1-fast"], {"default": "veo-3.1-fast"}),
            }
        }

    RETURN_TYPES = ("AF_PARAMS",)
    RETURN_NAMES = ("params",)
    FUNCTION = "pack"
    CATEGORY = "🚀Airforce/Modular"

    def pack(self, model):
        return ({"payload": {
            "model": model,
            "n": 1,
            "size": "1024x1024",
            "response_format": "url",
        }, },)


class AirforceWanParams:
    """Wan-2.6 video params; one reference image via wan_image_url."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": (["wan-2.6"], {"default": "wan-2.6"}),
                "aspectRatio": (["16:9", "9:16"], {"default": "16:9"}),
                "duration": ([5, 10, 15], {"default": 15}),
                "resolution": (["1080P", "720P"], {"default": "1080P"}),
                "sound": ("BOOLEAN", {"default": True, "label_on": "On", "label_off": "Off"}),
            },
            "optional": {
                "reference_urls": ("STRING", {"default": "", "placeholder": "From AnonDrop Upload, one URL per line, first used"}),
            }
        }

    RETURN_TYPES = ("AF_PARAMS",)
    RETURN_NAMES = ("params",)
    FUNCTION = "pack"
    CATEGORY = "🚀Airforce/Modular"

    def pack(self, model, aspectRatio, duration, resolution, sound, reference_urls=None):
        payload = {
            "model": model,
            "n": 1,
            "size": "1024x1024",
            "response_format": "url",
            "aspectRatio": aspectRatio,
            "duration": duration,
            "resolution": resolution,
            "sound": sound,
        }
        urls = parse_image_urls(reference_urls, max_count=1)
        if urls is not None and len(urls) > 0:
            payload["wan_image_url"] = urls[0]
        return ({"payload": payload, },)
