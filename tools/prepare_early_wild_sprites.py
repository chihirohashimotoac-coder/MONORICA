"""Export the reviewed first three wild-creature studies as sprite candidates."""
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
from prepare_starter_sprites import prepare

ROOT = Path(__file__).resolve().parents[1]


def main():
    config = json.loads((ROOT / "content/early-wild-art-export-profiles.json").read_text(encoding="utf-8"))
    files, report = {}, {"resampling": "nearest", "opaque_palette_limit_per_species": 31, "species": {}}
    for profile in config["profiles"]:
        new_files, details = prepare(profile)
        files.update(new_files)
        report["species"][profile["species_id"]] = details
    # All three families are validated before any output is written.
    for path, data in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    (ROOT / "reports/early-wild-sprite-geometry_v0.1.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"exported_files": len(files), "bytes_total": sum(len(d) for d in files.values()), "sha256": {str(p.relative_to(ROOT)): hashlib.sha256(d).hexdigest() for p, d in files.items()}}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
