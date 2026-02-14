# Publish checklist

Before pushing to GitHub and submitting to ComfyUI Manager:

## Repository structure

- [x] `__init__.py` — `NODE_CLASS_MAPPINGS` and `NODE_DISPLAY_NAME_MAPPINGS`
- [x] `config.py` / `params.py` / `upload.py` / `generator.py` — node logic
- [x] `requirements.txt` — requests, Pillow, numpy
- [x] `README.md` — install, usage, node list
- [x] `.gitignore` — `__pycache__`, `.cursor`, etc.

## Push to GitHub

1. Create a new GitHub repo, e.g. **ComfyUI-MyAirforce-Nodes**.
2. From the project folder:
   ```bash
   git init
   git add .
   git commit -m "Initial release: Airforce API nodes for ComfyUI"
   git remote add origin https://github.com/YOUR_USERNAME/ComfyUI-MyAirforce-Nodes.git
   git branch -M main
   git push -u origin main
   ```
3. Replace `YOUR_USERNAME` in README with your GitHub username.

## ComfyUI Manager (optional)

- Users can install anytime via Manager → **Install from GitHub** → paste repo URL.
- To appear in the Manager’s default list: fork [ComfyUI-Manager](https://github.com/Comfy-Org/ComfyUI-Manager), edit `custom-node-list.json` with your repo info, open a Pull Request.

## Optional

- Add a `LICENSE` file (e.g. MIT).
- Set repo Description and Topics on GitHub (e.g. comfyui, custom-nodes, airforce).
