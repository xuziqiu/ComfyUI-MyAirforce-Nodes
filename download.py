"""
独立下载节点：从 Submit 输出的 url 下载并保存到本地。
控件：保存目录（默认 ComfyUI output）、文件名前缀（默认 ComfyUI）。
"""
import os
import re
import requests
from io import BytesIO
from datetime import datetime

from PIL import Image


def _safe_filename_prefix(prefix):
    """只保留安全字符作为文件名前缀."""
    if not prefix or not str(prefix).strip():
        return "ComfyUI"
    s = re.sub(r'[<>:"/\\|?*]', "_", str(prefix).strip())
    return s[:64] if len(s) > 64 else s or "ComfyUI"


def download_and_save(url, directory, filename_prefix):
    """
    从 url 下载内容，根据类型保存为图片或视频。
    directory 为空时使用 ComfyUI 的 output 目录。
    返回 (saved_path, error_msg)。成功时 error_msg 为 None。
    """
    if not url or not str(url).strip():
        return ("", "URL 为空")

    try:
        resp = requests.get(url, timeout=60, stream=True)
        resp.raise_for_status()
        raw_bytes = resp.content
    except Exception as e:
        return ("", f"下载失败: {e}")

    try:
        import folder_paths
        base_dir = (directory and str(directory).strip()) or folder_paths.get_output_directory()
    except Exception:
        base_dir = directory and str(directory).strip() or os.path.expanduser("~")
    base_dir = os.path.normpath(base_dir)
    os.makedirs(base_dir, exist_ok=True)

    prefix = _safe_filename_prefix(filename_prefix)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 先尝试按图片解析，成功则存为 png
    try:
        img = Image.open(BytesIO(raw_bytes)).convert("RGB")
        out_path = os.path.join(base_dir, f"{prefix}_{stamp}.png")
        img.save(out_path)
        return (out_path, None)
    except Exception:
        pass

    # 否则按视频保存为 mp4
    try:
        out_path = os.path.join(base_dir, f"{prefix}_{stamp}.mp4")
        with open(out_path, "wb") as f:
            f.write(raw_bytes)
        return (out_path, None)
    except Exception as e:
        return ("", f"保存失败: {e}")


class AirforceDownload:
    """从 Submit 的 url 下载并保存：可设置保存目录与文件名前缀。默认使用 ComfyUI 的 output 目录，前缀 ComfyUI。"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "url": ("STRING", {"default": "", "forceInput": True}),
            },
            "optional": {
                "directory": ("STRING", {"default": "", "placeholder": "留空则使用 ComfyUI 的 output 目录"}),
                "filename_prefix": ("STRING", {"default": "ComfyUI"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("path",)
    FUNCTION = "download"
    CATEGORY = "🚀Airforce/Modular"
    OUTPUT_NODE = True  # 无下游节点时会执行，否则会被 ComfyUI 剪枝不跑

    def download(self, url, directory="", filename_prefix="ComfyUI"):
        path_str, err = download_and_save(url, directory, filename_prefix)
        # OUTPUT_NODE 可返回 ui 以在界面显示结果
        ui = {}
        if path_str:
            ui["text"] = [f"已保存: {path_str}"]
        elif err:
            ui["text"] = [f"失败: {err}"]
        return {"ui": ui, "result": (path_str,)}
