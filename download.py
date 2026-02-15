"""
Download node: fetches from Submit's url and saves locally.
Widgets: directory (default ComfyUI output), filename prefix (default ComfyUI).
"""
import os
import re
import requests
from io import BytesIO
from datetime import datetime

from PIL import Image


def _safe_filename_prefix(prefix):
    """Keep only safe characters for filename prefix."""
    if not prefix or not str(prefix).strip():
        return "ComfyUI"
    s = re.sub(r'[<>:"/\\|?*]', "_", str(prefix).strip())
    return s[:64] if len(s) > 64 else s or "ComfyUI"


def download_and_save(url, directory, filename_prefix):
    """
    Download from url and save as image or video. Uses ComfyUI output dir when directory is empty.
    Returns (saved_path, error_msg). error_msg is None on success.
    """
    if not url or not str(url).strip():
        return ("", "URL is empty")

    try:
        resp = requests.get(url, timeout=60, stream=True)
        resp.raise_for_status()
        raw_bytes = resp.content
    except Exception as e:
        return ("", f"Download failed: {e}")

    try:
        import folder_paths
        base_dir = (directory and str(directory).strip()) or folder_paths.get_output_directory()
    except Exception:
        base_dir = directory and str(directory).strip() or os.path.expanduser("~")
    base_dir = os.path.normpath(base_dir)
    os.makedirs(base_dir, exist_ok=True)

    prefix = _safe_filename_prefix(filename_prefix)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Try image first, save as png on success
    try:
        img = Image.open(BytesIO(raw_bytes)).convert("RGB")
        out_path = os.path.join(base_dir, f"{prefix}_{stamp}.png")
        img.save(out_path)
        return (out_path, None)
    except Exception:
        pass

    # Otherwise save as mp4
    try:
        out_path = os.path.join(base_dir, f"{prefix}_{stamp}.mp4")
        with open(out_path, "wb") as f:
            f.write(raw_bytes)
        return (out_path, None)
    except Exception as e:
        return ("", f"Save failed: {e}")


class AirforceDownload:
    """Download from Submit's url and save; optional directory and filename prefix. Default: ComfyUI output dir, prefix ComfyUI."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "url": ("STRING", {"default": "", "forceInput": True}),
            },
            "optional": {
                "directory": ("STRING", {"default": "", "placeholder": "Empty = ComfyUI output directory"}),
                "filename_prefix": ("STRING", {"default": "ComfyUI"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("path",)
    FUNCTION = "download"
    CATEGORY = "🚀Airforce/Modular"
    OUTPUT_NODE = True  # Run when no downstream nodes; otherwise ComfyUI may prune

    def download(self, url, directory="", filename_prefix="ComfyUI"):
        path_str, err = download_and_save(url, directory, filename_prefix)
        # OUTPUT_NODE can return ui to show result in the UI
        ui = {}
        if path_str:
            ui["text"] = [f"Saved: {path_str}"]
        elif err:
            ui["text"] = [f"Failed: {err}"]
        return {"ui": ui, "result": (path_str,)}
