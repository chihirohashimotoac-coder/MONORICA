"""Export the first Hanamimi candidates; source artwork is never overwritten.

Requires Pillow. This is a species-specific preparation experiment, not an
automatic quality guarantee for the remaining 155 species.
"""
from collections import deque
from io import BytesIO
from pathlib import Path
import hashlib
import json

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets/source/monsters/starter_flower_hare_01/pixel_study_v0.1.png"
SOURCE_SHA256 = "e88123b68ef6ec432252b674935e8946ced35594805235172595732e839f50df"
DEST = ROOT / "assets/runtime/monsters/starter_flower_hare_01"
# Pixel-space panels of the source study. The two large ears nearly touch;
# these explicit panels prevent a neighbouring creature entering the export.
PANELS = {"front": (0, 0, 840, 793), "back": (840, 0, 1500, 793), "icon": (1500, 0, 1983, 793)}


def largest_silhouette(image):
    """Keep the main 8-connected silhouette after a binary alpha threshold."""
    w, h = image.size
    alpha = image.getchannel("A").tobytes()
    remaining = {i for i, a in enumerate(alpha) if a >= 192}
    largest = set()
    while remaining:
        start = remaining.pop()
        component = {start}
        todo = deque([start])
        while todo:
            i = todo.popleft()
            x, y = i % w, i // w
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h:
                        other = ny * w + nx
                        if other in remaining:
                            remaining.remove(other)
                            component.add(other)
                            todo.append(other)
        if len(component) > len(largest):
            largest = component
    if not largest:
        raise ValueError("Empty source silhouette")
    cleaned = image.copy()
    cleaned.putalpha(Image.frombytes("L", image.size, bytes(255 if i in largest else 0 for i in range(w * h))))
    return cleaned.crop(cleaned.getbbox())


def inspect(image, kind):
    expected = (32, 32) if kind == "icon" else (96, 96)
    pad = 2 if kind == "icon" else 4
    w, h = image.size
    bbox = image.getbbox()
    alpha = set(image.getchannel("A").tobytes())
    opaque_colors = {p[:3] for p in image.get_flattened_data() if p[3]}
    assert image.mode == "RGBA" and image.size == expected
    assert alpha == {0, 255}, "Expected opaque pixel clusters and clear background"
    assert bbox and bbox[0] >= pad and bbox[1] >= pad and bbox[2] <= w - pad and bbox[3] <= h - pad
    assert len(opaque_colors) <= 31
    assert bbox[3] == (30 if kind == "icon" else 88)
    return {"size": list(image.size), "opaque_bbox": list(bbox), "opaque_colors": len(opaque_colors), "alpha_values": sorted(alpha), "ground_anchor": [w // 2, bbox[3]], "minimum_border_px": min(bbox[0], bbox[1], w - bbox[2], h - bbox[3])}


def main():
    raw = SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise ValueError("Source changed; review the crop and scale before rebuilding")
    source = Image.open(BytesIO(raw)).convert("RGBA")
    assert source.size == (1983, 793)
    crops = {kind: largest_silhouette(source.crop(rect)) for kind, rect in PANELS.items()}
    shared_scale = 80 / crops["front"].height
    patches = {}
    for kind, crop in crops.items():
        scale = 28 / crop.height if kind == "icon" else shared_scale
        patches[kind] = crop.resize((round(crop.width * scale), round(crop.height * scale)), Image.Resampling.NEAREST)
    # Only opaque pixels enter the shared palette; transparent black must not
    # displace eye, petal or outline colours. No dithering or soft alpha.
    colors = [p[:3] for patch in patches.values() for p in patch.get_flattened_data() if p[3]]
    sample = Image.new("RGB", (len(colors), 1))
    sample.putdata(colors)
    palette = sample.quantize(colors=31, method=Image.Quantize.MEDIANCUT)
    outputs = {}
    report = {"source": str(SOURCE.relative_to(ROOT)), "source_sha256": SOURCE_SHA256, "resampling": "nearest", "opaque_palette_limit": 31, "user_visual_review": "pending", "entries": {}}
    for kind, patch in patches.items():
        mask = patch.getchannel("A")
        patch = patch.convert("RGB").quantize(palette=palette, dither=Image.Dither.NONE).convert("RGBA")
        patch.putalpha(mask)
        # Centre the feet, rather than the wide ears, on the ground anchor.
        bbox = patch.getbbox()
        foot_y = bbox[3] - 1
        contacts = [x for x in range(patch.width) if mask.getpixel((x, foot_y))]
        contact_centre = round((min(contacts) + max(contacts)) / 2)
        size, ground = (32, 30) if kind == "icon" else (96, 88)
        target = Image.new("RGBA", (size, size))
        x, y = size // 2 - contact_centre, ground - bbox[3]
        if x < 0 or y < 0 or x + patch.width > size or y + patch.height > size:
            raise ValueError("Sprite does not fit; revise framing instead of clipping")
        target.paste(patch, (x, y), mask)
        info = inspect(target, kind)
        encoded = BytesIO()
        target.save(encoded, format="PNG", optimize=True)
        data = encoded.getvalue()
        path = DEST / (kind + ".png")
        if path.exists() and path.read_bytes() != data:
            raise FileExistsError(f"Preserving existing edited file: {path}")
        outputs[path] = data
        report["entries"][kind] = {**info, "path": str(path.relative_to(ROOT)), "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
    # All outputs are checked before writing any of them.
    DEST.mkdir(parents=True, exist_ok=True)
    for path, data in outputs.items():
        path.write_bytes(data)
    report_path = ROOT / "reports/hanamimi-sprite-geometry.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
