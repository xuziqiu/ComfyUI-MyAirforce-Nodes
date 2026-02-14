import json
import os
import torch
import numpy as np
import requests
from PIL import Image
from io import BytesIO
from datetime import datetime


def parse_size_from_payload(payload):
    """从 payload 的 size 解析宽高，返回 (w, h)，解析失败返回 (512, 512)。"""
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


def empty_img_batch(w=512, h=512):
    """返回空批次 tensor (0, H, W, 3)，用于失败时不输出任何图片，避免保存黑图。"""
    return torch.zeros((0, h, w, 3))


def run_one_generation(config, params, prompt):
    """
    执行一次生成请求。返回 (img_tensor 或 None, debug_req_str, debug_res_str, error_msg)。
    成功时 error_msg 为 None 且 img_tensor 为有效 tensor；失败时 img_tensor 为 None。
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
        response = requests.post(url, headers=headers, json=payload, stream=True, timeout=120)
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

        image_url = None
        if res_json and "data" in res_json and len(res_json["data"]) > 0:
            image_url = res_json["data"][0].get("url")

        if not image_url:
            return (None, debug_req_str, f"No image URL in SSE response:\n{debug_res_str}", None)

        try:
            img_response = requests.get(image_url, timeout=30)
            img_response.raise_for_status()
            img = Image.open(BytesIO(img_response.content)).convert("RGB")
        except Exception as e:
            return (None, debug_req_str, f"Download image failed: {e}", None)

        img_np = np.array(img).astype(np.float32) / 255.0
        img_tensor = torch.from_numpy(img_np).unsqueeze(0)
        return (img_tensor, debug_req_str, debug_res_str, None)

    except Exception as e:
        return (None, debug_req_str, f"Run error: {str(e)}", str(e))


def run_one_video_generation(config, params, prompt):
    """
    执行一次视频生成请求。返回 (video_path 或 "", debug_req_str, debug_res_str, error_msg)。
    成功时 error_msg 为 None 且 video_path 为非空路径；失败时 video_path 为 ""，不写入无效文件。
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
            return ("", debug_req_str, f"Error {response.status_code}:\n{debug_res_str}", None)

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

        video_url = None
        if res_json and "data" in res_json and len(res_json["data"]) > 0:
            video_url = res_json["data"][0].get("url")

        if not video_url:
            return ("", debug_req_str, f"No video URL in SSE response:\n{debug_res_str}", None)

        try:
            video_response = requests.get(video_url, timeout=60, stream=True)
            video_response.raise_for_status()
            video_bytes = video_response.content
        except Exception as e:
            return ("", debug_req_str, f"Download video failed: {e}", None)

        try:
            import folder_paths
            output_dir = folder_paths.get_output_directory()
            os.makedirs(output_dir, exist_ok=True)
            stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            out_path = os.path.join(output_dir, f"airforce_video_{stamp}.mp4")
            with open(out_path, "wb") as f:
                f.write(video_bytes)
        except Exception as e:
            return ("", debug_req_str, f"Save video failed: {e}", None)

        return (out_path, debug_req_str, debug_res_str, None)

    except Exception as e:
        return ("", debug_req_str, f"Run error: {str(e)}", str(e))


class AirforceGeneratorModular:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "config": ("AF_CONFIG",),
                "params": ("AF_PARAMS",),
                "prompt": ("STRING", {"multiline": True, "default": "a beautiful scenery", "placeholder": "Describe the image you want to generate"}),
            },
            "optional": {
                "random_seed": ("BOOLEAN", {"default": True, "label_on": "Random seed", "label_off": "Fixed"}),
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING", "STRING")
    RETURN_NAMES = ("image", "debug_request", "debug_response")
    FUNCTION = "generate"
    CATEGORY = "🚀Airforce/Modular"

    def generate(self, config, params, prompt, random_seed=True):
        # random_seed: not sent to API; when on, connect a Random node to break cache if you want rerun each time
        img_tensor, debug_req_str, debug_res_str, error_msg = run_one_generation(config, params, prompt)
        if img_tensor is None:
            w, h = parse_size_from_payload(params["payload"])
            # 失败时返回空批次 (0,H,W,3)，SaveImage 不会保存任何文件，避免浪费空间
            img_tensor = empty_img_batch(w, h)
        if error_msg is None:
            debug_res_str = (debug_res_str or "").rstrip() + "\n\nGenerated 1 image"
        return (img_tensor, debug_req_str, debug_res_str)


class AirforceVideoGeneratorModular:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "config": ("AF_CONFIG",),
                "params": ("AF_PARAMS",),
                "prompt": ("STRING", {"multiline": True, "default": "a beautiful scenery", "placeholder": "Describe the video you want to generate"}),
            },
            "optional": {
                "random_seed": ("BOOLEAN", {"default": True, "label_on": "Random seed", "label_off": "Fixed"}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("video_path", "debug_request", "debug_response")
    FUNCTION = "generate"
    CATEGORY = "🚀Airforce/Modular"

    def generate(self, config, params, prompt, random_seed=True):
        # random_seed: not sent to API; when on, connect a Random node to break cache if you want rerun each time
        video_path, debug_req_str, debug_res_str, error_msg = run_one_video_generation(config, params, prompt)
        if error_msg is None:
            debug_res_str = (debug_res_str or "").rstrip() + "\n\nGenerated 1 video"
        return (video_path or "", debug_req_str, debug_res_str)
