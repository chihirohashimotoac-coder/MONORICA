"""Prepare the two reviewed starter model designs as individual sprite candidates.

Uses reviewed per-source panels, not automatic guesses for other species.
Requires the same Pillow version as tools/requirements-art.txt.
"""
from io import BytesIO
from pathlib import Path
import hashlib
import json
import sys

sys.dont_write_bytecode = True
from PIL import Image
from prepare_hanamimi_sprites import largest_silhouette, inspect

ROOT = Path(__file__).resolve().parents[1]


def contact_centre(image, alignment="feet"):
    """Use the lowest band to include feet that are one row above the other."""
    if alignment == "bounds":
        return (image.width - 1) / 2
    mask = image.getchannel("A")
    top = max(0, image.height - max(2, round(image.height * 0.06)))
    xs = [x for y in range(top, image.height) for x in range(image.width) if mask.getpixel((x, y))]
    if not xs:
        raise ValueError("No ground-contact pixels")
    return (min(xs) + max(xs)) / 2


def starting_scale(images, max_height, capacity, alignment="feet"):
    limits = []
    for image in images.values():
        contact = contact_centre(image, alignment)
        limits.extend([max_height / image.height, capacity / max(1, contact), capacity / max(1, image.width - 1 - contact)])
    return min(limits)


def place(image, scale, kind, alignment="feet"):
    size, ground, pad = (32, 30, 2) if kind == "icon" else (96, 88, 4)
    width, height = max(1, round(image.width * scale)), max(1, round(image.height * scale))
    patch = image.resize((width, height), Image.Resampling.NEAREST)
    bbox = patch.getbbox()
    contact = round((contact_centre(image, alignment) + 0.5) * width / image.width - 0.5)
    x, y = size // 2 - contact, ground - bbox[3]
    if x < 0 or y < 0 or x + width > size or y + height > size:
        return None
    target = Image.new("RGBA", (size, size))
    target.paste(patch, (x, y), patch.getchannel("A"))
    bounds = target.getbbox()
    if not bounds or min(bounds[0], bounds[1], size - bounds[2], size - bounds[3]) < pad:
        return None
    return target


def prepare(profile):
    source_path = (ROOT / profile["source"]).resolve()
    if not source_path.is_relative_to(ROOT):
        raise ValueError("Source escapes the repository")
    raw = source_path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != profile["source_sha256"]:
        raise ValueError("Source changed; review export profile first")
    source = Image.open(BytesIO(raw)).convert("RGBA")
    if list(source.size) != profile["source_size"]:
        raise ValueError("Source dimensions changed")
    crops = {}
    for kind, panel in profile["panels"].items():
        crop = largest_silhouette(source.crop(panel))
        if profile["mirror_x"][kind]:
            crop = crop.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        crops[kind] = crop
    # Front/back use a common scale; wide wings get room instead of clipping.
    battle = {kind: crops[kind] for kind in ("front", "back")}
    scale = starting_scale(battle, 80, 43)
    for _ in range(30):
        placed = {kind: place(image, scale, kind) for kind, image in battle.items()}
        if all(image is not None for image in placed.values()):
            break
        scale *= 0.99
    else:
        raise ValueError("Battle sprite cannot fit without clipping")
    icon_alignment = profile.get("icon_alignment", "feet")
    icon_scale = starting_scale({"icon": crops["icon"]}, 28, 13, icon_alignment)
    for _ in range(30):
        icon = place(crops["icon"], icon_scale, "icon", icon_alignment)
        if icon is not None:
            break
        icon_scale *= 0.99
    else:
        raise ValueError("Icon cannot fit without clipping")
    placed["icon"] = icon
    opaque = [pixel[:3] for image in placed.values() for pixel in image.get_flattened_data() if pixel[3]]
    sample = Image.new("RGB", (len(opaque), 1))
    sample.putdata(opaque)
    palette = sample.quantize(colors=31, method=Image.Quantize.MEDIANCUT)
    files, report = {}, {"source": profile["source"], "source_sha256": profile["source_sha256"], "mirror_x": profile["mirror_x"], "battle_common_scale": scale, "icon_scale": icon_scale, "icon_alignment": icon_alignment, "state": "technical_checks_passed_visual_review_pending", "entries": {}}
    for kind, image in placed.items():
        alpha = image.getchannel("A")
        image = image.convert("RGB").quantize(palette=palette, dither=Image.Dither.NONE).convert("RGBA")
        image.putalpha(alpha)
        info = inspect(image, kind)
        buffer = BytesIO()
        image.save(buffer, format="PNG", optimize=True)
        data = buffer.getvalue()
        path = ROOT / "assets/runtime/monsters" / profile["species_id"] / (kind + ".png")
        if path.exists() and path.read_bytes() != data:
            raise FileExistsError("Preserving previously edited output: " + str(path))
        files[path] = data
        report["entries"][kind] = {**info, "path": str(path.relative_to(ROOT)), "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
    return files, report


def main():
    config = json.loads((ROOT / "content/starter-art-export-profiles.json").read_text(encoding="utf-8"))
    files, report = {}, {"resampling": "nearest", "opaque_palette_limit_per_species": 31, "species": {}}
    for profile in config["profiles"]:
        new_files, details = prepare(profile)
        files.update(new_files)
        report["species"][profile["species_id"]] = details
    # Validate both families before writing either family.
    for path, data in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    (ROOT / "reports/starter-sprite-geometry_v0.1.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
