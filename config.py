# 配置与常量

# 比例预设：各参数节点共用，按「横:竖」排序便于选择
ASPECT_RATIO_PRESETS = [
    "1:1",
    "4:3", "3:4",
    "16:9", "9:16",
    "3:2", "2:3",
    "5:4", "4:5",
    "21:9", "9:21",
    "2:1", "1:2",
    "5:7", "7:5",
    "16:10", "10:16",
]

# 每个系列: models = 可选模型名列表, payload_keys = 该系列在节点中暴露的参数字段
MODEL_REGISTRY = {
    "nano": {
        "models": ["nano-banana-pro"],
        "payload_keys": ["model", "n", "size", "aspectRatio", "resolution"],
    },
    "flux": {
        "models": ["flux-2-pro", "flux-2-dev", "flux-2-flex", "flux-2-klein-9b", "flux-2-klein-4b"],
        "payload_keys": ["model", "n", "size", "aspectRatio", "resolution"],
    },
}

# Flux Pro/Flex 使用比例+分辨率；Klein/Dev 使用宽高
FLUX_PRO_FLEX = ("flux-2-pro", "flux-2-flex")


class AirforceConfig:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "base_url": ("STRING", {"default": "https://api.airforce/v1", "placeholder": "API base URL e.g. https://api.xxx/v1"}),
                "api_key": ("STRING", {"default": "sk-...", "placeholder": "API key (sk-...)"}),
            },
            "optional": {
                "anondrop_key": ("STRING", {"default": "", "placeholder": "AnonDrop API Key (for reference upload)"}),
                "anondrop_base_url": ("STRING", {"default": "https://anondrop.net", "placeholder": "AnonDrop base URL"}),
            }
        }

    RETURN_TYPES = ("AF_CONFIG",)
    RETURN_NAMES = ("config",)
    FUNCTION = "setup"
    CATEGORY = "🚀Airforce/Modular"

    def setup(self, base_url, api_key, anondrop_key="", anondrop_base_url="https://anondrop.net"):
        cfg = {
            "base_url": base_url.strip().rstrip("/"),
            "api_key": api_key.strip(),
            "anondrop_key": (anondrop_key or "").strip(),
            "anondrop_base_url": (anondrop_base_url or "https://anondrop.net").strip().rstrip("/"),
        }
        return (cfg,)
