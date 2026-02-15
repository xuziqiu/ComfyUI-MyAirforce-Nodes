import re
import torch
import numpy as np
import requests
from PIL import Image
from io import BytesIO


def parse_image_urls(text, max_count=8):
    """Parse reference image URLs from newline or comma-separated string; at most max_count."""
    if not text or not str(text).strip():
        return None
    urls = []
    for part in str(text).replace(",", "\n").splitlines():
        u = part.strip()
        if u and len(urls) < max_count:
            urls.append(u)
    return urls if urls else None


def image_tensor_to_png_bytes(tensor):
    """ComfyUI IMAGE tensor (1,H,W,C) or (H,W,C) float 0-1 to PNG bytes."""
    if tensor.dim() == 4:
        tensor = tensor[0]
    arr = tensor.cpu().numpy()
    if arr.max() <= 1.0:
        arr = (arr * 255).clip(0, 255).astype(np.uint8)
    else:
        arr = arr.clip(0, 255).astype(np.uint8)
    pil = Image.fromarray(arr)
    buf = BytesIO()
    pil.save(buf, format="PNG")
    return buf.getvalue()


def anondrop_extract_url(response):
    """Extract file URL from AnonDrop upload response (JSON or plain link)."""
    text = response.text.strip()
    try:
        data = response.json()
        for key in ("url", "file_url", "directUrl", "link", "fileUrl"):
            if isinstance(data.get(key), str) and data[key].startswith("http"):
                return data[key]
        if "file" in data and isinstance(data["file"], dict):
            u = data["file"].get("url") or data["file"].get("link")
            if u and str(u).startswith("http"):
                return u
    except Exception:
        pass
    m = re.search(r"https?://[^\s\"'<>]+", text)
    if m:
        return m.group(0).rstrip(".,;:)")
    return None


class AirforceAnonDropUpload:
    @classmethod
    def INPUT_TYPES(cls):
        inputs = {
            "required": {
                "config": ("AF_CONFIG",),
            },
            "optional": {}
        }
        for i in range(1, 15):
            inputs["optional"][f"image_{i}"] = ("IMAGE",)
        return inputs

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("reference_urls", "status")
    FUNCTION = "upload"
    CATEGORY = "🚀Airforce/Modular"

    def upload(self, config, **kwargs):
        key = (config.get("anondrop_key") or "").strip()
        if not key:
            return ("", "No AnonDrop Key (set in Config node)")
        base = (config.get("anondrop_base_url") or "https://anondrop.net").strip().rstrip("/")
        upload_url = f"{base}/upload"
        urls = []
        errors = []
        for i in range(1, 15):
            img = kwargs.get(f"image_{i}")
            if img is None:
                continue
            if isinstance(img, torch.Tensor) and img.numel() > 0:
                try:
                    png_bytes = image_tensor_to_png_bytes(img)
                except Exception as e:
                    errors.append(f"image_{i} convert failed: {e}")
                    continue
            else:
                continue
            try:
                r = requests.post(
                    upload_url,
                    params={"key": key},
                    files={"file": (f"ref_{i}.png", png_bytes, "image/png")},
                    timeout=60,
                )
                if r.status_code != 200:
                    errors.append(f"image_{i} upload HTTP {r.status_code}: {r.text[:200]}")
                    continue
                u = anondrop_extract_url(r)
                if u:
                    urls.append(u.rstrip("/") + "/img.png")
                else:
                    errors.append(f"image_{i} no URL in response: {r.text[:200]}")
            except Exception as e:
                errors.append(f"image_{i} request error: {e}")
        reference_urls = "\n".join(urls)
        status = "Uploaded " + str(len(urls)) + " image(s)" if urls else "No images uploaded"
        if errors:
            status += "; " + "; ".join(errors[:3])
            if len(errors) > 3:
                status += " ..."
        return (reference_urls, status)
