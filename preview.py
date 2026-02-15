class AirforceVideoPreview:
    """Video preview only: takes URL, frontend renders HTML5 video in the node (image URLs are ignored)."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "url": ("STRING", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "preview"
    OUTPUT_NODE = True
    CATEGORY = "🚀Airforce/Modular"

    def preview(self, url):
        return {"ui": {"video_url": [url]}, "result": (url,)}
