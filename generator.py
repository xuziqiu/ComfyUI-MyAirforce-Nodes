import json
import random
import torch
import numpy as np
import requests
from PIL import Image
from io import BytesIO


def parse_size_from_payload(payload):
    """Parse width/height from payload size; return (w, h) or (512, 512) on failure."""
    size = payload.get("size") or ""
    if isinstance(size, str) and "x" in size:
        parts = size.strip().lower().split("x")
        if len(parts) == 2:
            try:
                w, h = int(parts[0].strip()), int(parts[1].strip())
                if 64 <= w <= 4096 and 64 <= h <= 4096:
                    return (w, h)
            except ValueError:
                pass
    return (512, 512)


def placeholder_img_batch(w=512, h=512):
    """Single-frame placeholder (1, H, W, 3) for display in node when there is no image. Not written to disk by this node; avoids index-0 errors in preview/downstream. If connected to SaveImage, that node will save it."""
    return torch.zeros((1, h, w, 3))


def run_one_request(config, params, prompt):
    """
    Single API request + SSE parse. Returns (content_url or None, debug_req_str, debug_res_str, error_msg).
    On success error_msg is None and content_url is set; on failure content_url is None.
    """
    url = f"{config['base_url']}/images/generations"
    headers = {
        "Authorization": f"Bearer {config['api_key']}",
        "Content-Type": "application/json"
    }
    payload = params["payload"].copy()
    payload["prompt"] = prompt
    payload["sse"] = True

    debug_req_info = {
        "url": url,
        "method": "POST",
        "headers": {"Authorization": "Bearer sk-air-***"},
        "body": payload
    }
    debug_req_str = json.dumps(debug_req_info, indent=2, ensure_ascii=False)

    try:
        response = requests.post(url, headers=headers, json=payload, stream=True, timeout=180)
        if response.status_code != 200:
            debug_res_str = response.text
            try:
                debug_res_str = json.dumps(response.json(), indent=2, ensure_ascii=False)
            except Exception:
                pass
            return (None, debug_req_str, f"Error {response.status_code}:\n{debug_res_str}", None)

        res_json = None
        sse_lines = []
        for line in response.iter_lines():
            if not line:
                continue
            line_str = line.decode("utf-8")
            if not line_str.startswith("data: "):
                continue
            if line_str == "data: [DONE]" or line_str == "data: : keepalive":
                continue
            try:
                data = json.loads(line_str[6:])
                res_json = data
                sse_lines.append(data)
            except Exception:
                continue

        debug_res_str = json.dumps(sse_lines, indent=2, ensure_ascii=False) if sse_lines else "[]"

        content_url = None
        if res_json and "data" in res_json and len(res_json["data"]) > 0:
            content_url = res_json["data"][0].get("url")

        if not content_url:
            return (None, debug_req_str, f"No URL in SSE response:\n{debug_res_str}", None)

        return (content_url, debug_req_str, debug_res_str, None)

    except Exception as e:
        return (None, debug_req_str, f"Run error: {str(e)}", str(e))


def _fetch_and_detect(config, params, prompt):
    """
    Request API, fetch content in memory only (no save to disk). Try to parse as image for tensor; else treat as video.
    Returns (img_tensor, content_url, debug_req_str, debug_res_str). path is always ""; use Airforce Download node to save from url.
    """
    content_url, debug_req_str, debug_res_str, error_msg = run_one_request(config, params, prompt)
    w, h = parse_size_from_payload(params["payload"])
    placeholder = placeholder_img_batch(w, h)

    if content_url is None:
        if error_msg is None:
            debug_res_str = (debug_res_str or "").rstrip() + "\n\nRequest failed (no URL)"
        return (placeholder, "", debug_req_str, debug_res_str)

    try:
        resp = requests.get(content_url, timeout=60, stream=True)
        resp.raise_for_status()
        raw_bytes = resp.content
    except Exception as e:
        debug_res_str = (debug_res_str or "").rstrip() + f"\n\nDownload failed: {e}"
        return (placeholder, "", debug_req_str, debug_res_str)

    # Try to parse as image for preview tensor (no save)
    try:
        img = Image.open(BytesIO(raw_bytes)).convert("RGB")
        img_np = np.array(img).astype(np.float32) / 255.0
        img_tensor = torch.from_numpy(img_np).unsqueeze(0)
        debug_res_str = (debug_res_str or "").rstrip() + "\n\nGenerated 1 image"
        return (img_tensor, content_url, debug_req_str, debug_res_str)
    except Exception:
        pass

    # Video: return placeholder and url; save via Download node
    debug_res_str = (debug_res_str or "").rstrip() + "\n\nGenerated 1 video"
    return (placeholder, content_url, debug_req_str, debug_res_str)


class AirforceGeneratorModular:
    """Unified image/video submit: request API and return image tensor (for preview), url, and debug. Does not save to disk; connect url to Airforce Download to save file."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "config": ("AF_CONFIG",),
                "params": ("AF_PARAMS",),
                "prompt": ("STRING", {"multiline": True, "default": "a beautiful scenery", "placeholder": "Describe the image or video you want to generate"}),
            },
            "optional": {
                "random_seed": ("BOOLEAN", {"default": True, "label_on": "Random seed", "label_off": "Fixed"}),
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("image", "path", "url", "debug_request", "debug_response")
    FUNCTION = "generate"
    CATEGORY = "🚀Airforce/Modular"

    @classmethod
    def IS_CHANGED(cls, random_seed=True, **kwargs):
        # When Random seed is on, return a different value each time so the node is treated as changed and cache is bypassed
        if random_seed:
            return random.random()
        return "fixed"

    def generate(self, config, params, prompt, random_seed=True):
        img_tensor, content_url, debug_req_str, debug_res_str = _fetch_and_detect(config, params, prompt)
        # path is left empty; use Download node to save from url
        return (img_tensor, "", content_url or "", debug_req_str, debug_res_str)
