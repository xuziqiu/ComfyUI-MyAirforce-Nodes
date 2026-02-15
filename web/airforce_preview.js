import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";

function isVideoUrl(url) {
    if (!url || typeof url !== "string") return false;
    const u = url.split("?")[0].toLowerCase();
    return /\.(mp4|webm|mov|ogg|ogv|m4v)(\?|$)/i.test(u) || /\/video\//i.test(u);
}

const DEFAULT_WIDGET_HEIGHT = 280;
const NODE_TITLE_OFFSET = 50;
const AF_NODE_ID_ATTR = "data-af-node-id";

function applyContentSize(node, contentW, contentH, resolutionDiv) {
    if (resolutionDiv) resolutionDiv.textContent = contentW + " x " + contentH;
    node.setDirtyCanvas(true, true);
}

// Remove all preview DOM for this node id from the document (avoids old video left in other layers / not scaling with box)
function removeAllPreviewDomByNodeId(nodeId) {
    const id = String(nodeId);
    document.querySelectorAll(".airforce-preview-outer[" + AF_NODE_ID_ATTR + "=\"" + id + "\"]").forEach(function (el) {
        const v = el.querySelector("video");
        if (v) {
            v.pause();
            v.removeAttribute("src");
            v.load();
        }
        el.remove();
    });
}

function removeAllAfPlayerWidgets(node) {
    if (!node.widgets) return;
    while (true) {
        const idx = node.widgets.findIndex(w => w.name === "af_player");
        if (idx === -1) break;
        const w = node.widgets[idx];
        if (w.canvas) {
            w.canvas.removeAttribute(AF_NODE_ID_ATTR);
            const video = w.canvas.querySelector("video");
            if (video) {
                video.pause();
                video.removeAttribute("src");
                video.load();
            }
            if (w.canvas.parentNode) w.canvas.parentNode.removeChild(w.canvas);
            else if (w.canvas.remove) w.canvas.remove();
        }
        node.widgets.splice(idx, 1);
        if (w.onRemoved) w.onRemoved();
    }
}

function applyVideoPreviewToNode(node, mediaUrl) {
    if (!node) return;
    if (!node.widgets) node.widgets = [];

    const nodeId = node.id;

    if (!mediaUrl || !isVideoUrl(mediaUrl)) {
        removeAllPreviewDomByNodeId(nodeId);
        removeAllAfPlayerWidgets(node);
        node._af_preview_url = null;
        if (node.graph && node.graph.setDirtyCanvas) node.graph.setDirtyCanvas(true, true);
        return;
    }

    node._af_preview_url = mediaUrl;

    // Clear any stale preview DOM in other layers (stacked below, not scaling with box)
    removeAllPreviewDomByNodeId(nodeId);

    const existing = node.widgets.find(w => w.name === "af_player");
    if (existing && existing.canvas && document.contains(existing.canvas)) {
        existing.canvas.setAttribute(AF_NODE_ID_ATTR, String(nodeId));
        const video = existing.canvas.querySelector("video");
        const resolutionDiv = existing.canvas.querySelector(".airforce-preview-resolution");
        if (video) {
            if (resolutionDiv) resolutionDiv.textContent = "";
            video.pause();
            video.src = mediaUrl;
            video.load();
            video.play().catch(() => {});
        }
        if (!node.size || node.size[0] < 100) node.setSize([320, 280]);
        if (node.graph && node.graph.setDirtyCanvas) node.graph.setDirtyCanvas(true, true);
        return;
    }

    removeAllAfPlayerWidgets(node);

    const resolutionDiv = document.createElement("div");
    resolutionDiv.className = "airforce-preview-resolution";
    resolutionDiv.style.cssText = "margin-top: 4px; font-size: 11px; color: var(--input-text, #888); line-height: 1.2; flex-shrink: 0;";
    resolutionDiv.textContent = "";

    const elem = document.createElement("video");
    elem.style.width = "100%";
    elem.style.height = "100%";
    elem.style.objectFit = "contain";
    elem.style.display = "block";
    elem.style.pointerEvents = "auto";
    elem.controls = true;
    elem.autoplay = true;
    elem.loop = true;
    elem.src = mediaUrl;
    elem.addEventListener("loadedmetadata", function () {
        if (elem.videoWidth) applyContentSize(node, elem.videoWidth, elem.videoHeight, resolutionDiv);
    });
    elem.addEventListener("error", function () {
        resolutionDiv.textContent = "";
    });

    const previewArea = document.createElement("div");
    previewArea.style.cssText = "flex: 1; min-height: 0; overflow: hidden; display: flex; align-items: center; justify-content: center; width: 100%; pointer-events: auto; transition: none;";
    previewArea.appendChild(elem);

    const outer = document.createElement("div");
    outer.className = "airforce-preview-outer";
    outer.setAttribute(AF_NODE_ID_ATTR, String(nodeId));
    outer.style.cssText = "pointer-events: none; width: 100%; height: 100%; display: flex; flex-direction: column; box-sizing: border-box; min-height: 0; flex-shrink: 1; overflow: hidden; transition: none;";
    outer.appendChild(previewArea);
    outer.appendChild(resolutionDiv);

    const added = node.addDOMWidget("af_player", "", outer);
    if (added && typeof added.computeSize === "undefined") {
        added.computeSize = function (width) {
            const h = (node.size && node.size[1] > 0) ? node.size[1] - NODE_TITLE_OFFSET : DEFAULT_WIDGET_HEIGHT;
            const height = Math.max(0, h);
            if (this.canvas) {
                this.canvas.style.setProperty("width", width + "px", "important");
                this.canvas.style.setProperty("height", height + "px", "important");
                this.canvas.style.setProperty("min-height", "0", "important");
            }
            return [width, height];
        };
    }

    if (!node.size || node.size[0] < 100) node.setSize([320, 280]);
    if (node.graph && node.graph.setDirtyCanvas) node.graph.setDirtyCanvas(true, true);
}

function findGraphNodeById(graph, nodeId) {
    if (!graph || nodeId == null) return null;
    if (typeof graph.getNodeById === "function") {
        const n = graph.getNodeById(nodeId);
        if (n) return n;
    }
    const id = Number(nodeId);
    if (!Number.isNaN(id) && graph._nodes) {
        const found = graph._nodes.find(n => n.id === id || n.id === nodeId);
        if (found) return found;
    }
    if (graph._nodes) {
        return graph._nodes.find(n => n.id === nodeId || String(n.id) === String(nodeId)) || null;
    }
    return null;
}

app.registerExtension({
    name: "Airforce.Preview",
    setup() {
        api.addEventListener("executed", function (ev) {
            const detail = ev.detail;
            if (!detail || !detail.output) return;
            const list = detail.output.video_url;
            const mediaUrl = Array.isArray(list) && list.length > 0 ? list[0] : null;
            const graph = app.graph;
            if (!graph) return;
            const node = findGraphNodeById(graph, detail.node);
            const isPreview = node && (node.type === "AirforceVideoPreview" || node.comfyClass === "AirforceVideoPreview");
            if (!isPreview) return;
            applyVideoPreviewToNode(node, mediaUrl);
        });
    },
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "AirforceVideoPreview") {
            const onExecuted = nodeType.prototype.onExecuted;
            nodeType.prototype.onExecuted = function (message) {
                onExecuted?.apply(this, arguments);
            };
            const origOnResize = nodeType.prototype.onResize;
            nodeType.prototype.onResize = function (size) {
                if (origOnResize) origOnResize.apply(this, arguments);
                const w = this.widgets && this.widgets.find(x => x.name === "af_player");
                if (w && w.canvas && size && size[0] > 0 && size[1] > 0) {
                    const h = Math.max(0, size[1] - NODE_TITLE_OFFSET);
                    w.canvas.style.setProperty("width", size[0] + "px", "important");
                    w.canvas.style.setProperty("height", h + "px", "important");
                    w.canvas.style.setProperty("min-height", "0", "important");
                }
                if (this.graph && this.graph.setDirtyCanvas) this.graph.setDirtyCanvas(true, true);
            };

            const origGetExtra = nodeType.prototype.getExtraMenuOptions;
            nodeType.prototype.getExtraMenuOptions = function (_, options) {
                const r = origGetExtra ? origGetExtra.apply(this, arguments) : (options || []);
                const url = this._af_preview_url;
                if (url && Array.isArray(options)) {
                    options.unshift({ content: "Open preview in new tab", callback: () => window.open(url, "_blank") });
                }
                return r;
            };
        }
    }
});
