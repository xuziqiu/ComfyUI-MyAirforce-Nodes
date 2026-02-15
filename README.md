# ComfyUI-MyAirforce-Nodes

ComfyUI custom nodes for **Airforce** API: image and video generation with multiple models (Nano, Flux, Imagen, Z-Image, Seedream, Suno, Grok Imagine Video, Veo, Wan), plus reference image upload via AnonDrop.

---

## Features

- **Config node**: Set API base URL and API key; optional AnonDrop key for reference uploads.
- **Parameter nodes**: Per-model params (NanoBanana, Flux Pro/Flex, Flux Dev/Klein, Z-Image, Imagen, Seedream, Suno, Grok Imagine Video, Veo, Wan). In the node list, 🎨 = image params, 🎬 = video params.
- **Reference upload**: Upload ComfyUI images to AnonDrop and get URLs for image/video models that support references.
- **Submit node** (one node for both): Config + params + prompt → **image** (IMAGE tensor; placeholder for video), **path** (always empty), **url**, and debug outputs. Connect **url** to **Airforce: Download** to save file; connect **url** to **Airforce Previewer** for in-node video preview. Image vs video is detected from API response.

All nodes live under category **🚀Airforce/Modular**.

---

## Installation

### Option 1: ComfyUI Manager (recommended)

1. Open ComfyUI → **Manager** tab.
2. Click **Install Custom Nodes** (or **Install from GitHub**).
3. Paste this repo URL and install:
   ```
   https://github.com/xuziqiu/ComfyUI-MyAirforce-Nodes
   ```
4. Restart ComfyUI or refresh the node list.

### Option 2: Manual

1. Clone into your ComfyUI `custom_nodes` folder:
   ```bash
   cd ComfyUI/custom_nodes
   git clone https://github.com/xuziqiu/ComfyUI-MyAirforce-Nodes.git
   ```
2. Install dependencies:
   ```bash
   cd ComfyUI-MyAirforce-Nodes
   pip install -r requirements.txt
   ```
3. Restart ComfyUI.

---

## Example Workflows

Pre-built workflows are in `example_workflows/`. In ComfyUI, go to **Workflow** → **Browse Templates** and select **ComfyUI-MyAirforce-Nodes** to load them.

---

## Requirements

- ComfyUI (with PyTorch).
- Python dependencies are in `requirements.txt`: `requests`, `Pillow`, `numpy` (torch comes from ComfyUI).

---

## Repository structure

```
ComfyUI-MyAirforce-Nodes/
├── example_workflows/   # Pre-built workflows (load via Workflow → Browse Templates)
├── __init__.py         # Entry: NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS
├── config.py           # AirforceConfig, constants, model registry
├── params.py         # All *Params nodes (Nano, Flux, Z-Image, Imagen, etc.)
├── upload.py         # AnonDrop upload node and URL parsing
├── generator.py      # Unified image/video Submit node
├── download.py       # AirforceDownload node
├── preview.py        # AirforceVideoPreview node (in-node video preview)
├── web/
│   └── airforce_preview.js  # Frontend: in-node preview widget
├── requirements.txt  # requests, Pillow, numpy
├── README.md         # This file
└── .gitignore        # __pycache__, .cursor, etc.
```

---

## Node list

| Node | Description |
|------|-------------|
| ⚙️ Airforce: Config | API base URL, API key, AnonDrop key/URL |
| 📤 Reference: AnonDrop Upload | Upload images → reference URLs string |
| 🎨 NanoBanana | nano-banana-pro params (image) |
| 🎨 Flux Pro/Flex | flux-2-pro, flux-2-flex (image) |
| 🎨 Flux Dev/Klein | flux-2-dev, flux-2-klein-9b/4b (image) |
| 🎨 Z-Image | z-image (image) |
| 🎨 Imagen | imagen-3, imagen-4 (image) |
| 🎨 Seedream | seedream-4.5 (image) |
| 🎬 Suno | suno-v5, suno-4.5 (video) |
| 🎬 Grok Imagine | grok-imagine-video (video) |
| 🎬 Veo | veo-3.1-fast (video) |
| 🎬 Wan | wan-2.6 (video) |
| 🎯 Airforce: Submit | Run generation → **image**, **path**, **url**, debug. Does not save to disk. With **Random seed** on, each Queue Prompt bypasses cache and re-requests (via IS_CHANGED). |
| ⬇️ Airforce: Download | Input **url** → downloads and saves as PNG or MP4. Outputs **path** to saved file. Uses ComfyUI output dir by default. |
| 📺 Airforce Previewer | Input **url** → in-node HTML5 video preview (video URLs only). Connect Submit **url** for playback. |

---

## Usage (minimal)

1. Add **Airforce: Config**, fill base URL and API key.
2. Add one **Params** node for your model (🎨 for image, 🎬 for video).
3. Add **Airforce: Submit**; connect config, params, and a prompt. Connect **image** to **Preview Image** to view images; connect **url** to **Airforce: Download** to save file (PNG or MP4); connect **url** to **Airforce Previewer** for in-node video preview (video only).
4. For reference images: add **Reference: AnonDrop Upload**, connect config and images, then paste the output URLs into the Params node’s reference field (if supported).

---

## Publishing to ComfyUI Manager (for maintainers)

To list this pack in the Manager’s default list:

1. Fork [ComfyUI-Manager](https://github.com/Comfy-Org/ComfyUI-Manager).
2. Edit `custom-node-list.json`: add an entry with your repo URL and a short description.
3. Open a Pull Request; after merge, the node pack will appear in the Manager for all users.

Users can still install via **Install from GitHub** with your repo URL even before the PR is merged.

---

## License

Use the same license as your project (e.g. MIT). Add a `LICENSE` file in the repo if you publish.
