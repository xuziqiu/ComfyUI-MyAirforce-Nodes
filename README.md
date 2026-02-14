# ComfyUI-MyAirforce-Nodes

ComfyUI custom nodes for **Airforce** API: image and video generation with multiple models (Nano, Flux, Imagen, Z-Image, Seedream, Suno, Grok Imagine Video, Veo, Wan), plus reference image upload via AnonDrop.

---

## Features

- **Config node**: Set API base URL and API key; optional AnonDrop key for reference uploads.
- **Parameter nodes**: Per-model params (NanoBanana, Flux Pro/Flex, Flux Dev/Klein, Z-Image, Imagen, Seedream, Suno, Grok Imagine Video, Veo, Wan).
- **Reference upload**: Upload ComfyUI images to AnonDrop and get URLs for image/video models that support references.
- **Image generator**: Submit with config + params + prompt → IMAGE + debug outputs.
- **Video generator**: Same flow → video file path + debug outputs.

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

## Requirements

- ComfyUI (with PyTorch).
- Python dependencies are in `requirements.txt`: `requests`, `Pillow`, `numpy` (torch comes from ComfyUI).

---

## Repository structure

```
ComfyUI-MyAirforce-Nodes/
├── __init__.py       # Entry: NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS
├── config.py         # AirforceConfig, constants, model registry
├── params.py         # All *Params nodes (Nano, Flux, Z-Image, Imagen, etc.)
├── upload.py         # AnonDrop upload node and URL parsing
├── generator.py      # Image and video generator nodes
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
| 📝 NanoBanana (Image) | nano-banana-pro params |
| 📝 Flux Pro/Flex (Image) | flux-2-pro, flux-2-flex |
| 📝 Flux Dev/Klein (Image) | flux-2-dev, flux-2-klein-9b/4b |
| 📝 Z-Image (Image) | z-image |
| 📝 Imagen (Image) | imagen-3, imagen-4 |
| 📝 Seedream (Image) | seedream-4.5 |
| 📝 Suno (Video) | suno-v5, suno-4.5 |
| 📝 Grok Imagine (Video) | grok-imagine-video |
| 📝 Veo (Video) | veo-3.1-fast |
| 📝 Wan (Video) | wan-2.6 |
| 🎨 Airforce: Submit (Image) | Run image generation → IMAGE + debug |
| 🎬 Airforce: Submit (Video) | Run video generation → video path + debug |

---

## Usage (minimal)

1. Add **Airforce: Config**, fill base URL and API key.
2. Add one **Params** node for your model (e.g. **Flux Pro/Flex**).
3. Add **Airforce: Submit (Image)** or **Submit (Video)**; connect config, params, and a prompt.
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
