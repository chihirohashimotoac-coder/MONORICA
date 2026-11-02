"""Validate planning references and counts; never claim the game is complete."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    errors = []

    def check(ok, message):
        if not ok:
            errors.append(message)

    def read(path):
        return json.loads((ROOT / path).read_text(encoding="utf-8"))

    world = read("content/planning/world-outline.json")
    cards = read("content/planning/known-species.json")
    assets = read("manifests/assets.json")
    types = set(read("content/type-chart.json")["type_order"])
    regions = world["regions"]
    region_ids = {r["id"] for r in regions}
    check(len(region_ids) == len(regions), "Duplicate region ID")
    main_regions = [r for r in regions if r["phase"] == "main_story"]
    post_regions = [r for r in regions if r["phase"] == "postgame"]
    check(len(main_regions) == world["target_main_regions"] == 8, "Main region count")
    check(len(post_regions) == world["target_postgame_regions"] == 2, "Postgame region count")
    reps = [r["representative"]["id"] for r in main_regions if r["representative"]]
    check(len(set(reps)) == len(reps) == world["target_representatives"] == 8, "Representative count/IDs")
    check(world["starter_species_slots"] + sum(r["new_species_slots"] for r in regions) == world["target_species_count"] == 156, "Species allocation sum")
    check(sum(r["estimated_map_units"] for r in regions) + world["additional_map_units"] == 60, "Map estimate sum")
    for a, b in world["route_edges"]:
        check(a in region_ids and b in region_ids, "Unknown route endpoint")
    for r in regions:
        check(all(x in region_ids or x == "chapter_final" for x in r["unlocks_after"]), "Unknown progression reference")
    asset_ids = {a["id"] for a in assets["entries"]}
    species = cards["species"]
    by_id = {s["id"]: s for s in species}
    check(len(by_id) == len(species) == 15, "Known production cards count/IDs")
    evolution_count = 0
    for s in species:
        check(s["reference_asset_id"] in asset_ids, "Unknown source asset: " + s["id"])
        check(s["primary_type_candidate"] in types, "Unknown type: " + s["id"])
        nxt = s["evolves_to"]
        if nxt:
            target = by_id.get(nxt["id"])
            check(target is not None, "Unknown evolution target: " + s["id"])
            if target:
                check(target["family_id"] == s["family_id"] and target["stage"] == s["stage"] + 1, "Evolution family/stage mismatch")
            check(nxt["method"] == "level" and nxt["level"] == (16 if s["stage"] == 1 else 36), "Changed confirmed starter level")
            evolution_count += 1
    check(evolution_count == 6, "Starter evolution link count")
    with (ROOT / "content/planning/audio-cues.csv").open(encoding="utf-8", newline="") as f:
        cues = list(csv.DictReader(f))
    check(len({x["id"] for x in cues}) == len(cues) == 28, "BGM cue IDs/count")
    check(all(x["state"] == "not_generated" and not x["runtime_path"] and not x["loop_samples"] for x in cues), "Unverified music must stay ungenerated")
    with (ROOT / "manifests/production_queue.csv").open(encoding="utf-8", newline="") as f:
        queue = list(csv.DictReader(f))
    check(len({x["id"] for x in queue}) == len(queue), "Duplicate queue ID")
    for x in queue:
        check((ROOT / x["planned_path"]).resolve().is_relative_to(ROOT), "Invalid planned output path")
        if x["state"] == "not_created":
            check(not (ROOT / x["planned_path"]).exists(), "Queue says not_created but file exists: " + x["id"])
        else:
            check((ROOT / x["planned_path"]).is_file(), "Created queue entry is missing: " + x["id"])
    runtime_pngs = list((ROOT / "assets/runtime").rglob("*.png"))
    audio_files = [p for p in (ROOT / "assets/runtime").rglob("*") if p.suffix.lower() in {".mp3", ".ogg", ".wav", ".m4a", ".aac"}]
    check(len(runtime_pngs) == assets["runtime_image_count"], "Runtime PNG count")
    recorded_runtime_pngs = {str((ROOT / a["path"]).resolve()) for a in assets["entries"] if a["path"].startswith("assets/runtime/") and a["path"].endswith(".png")}
    check(recorded_runtime_pngs == {str(p.resolve()) for p in runtime_pngs}, "Unrecorded or missing runtime PNG")
    ready_pngs = [a for a in assets["entries"] if a["path"].startswith("assets/runtime/") and a["path"].endswith(".png") and a.get("runtime_ready")]
    check(len(ready_pngs) == assets.get("runtime_ready_image_count", 0), "Ready PNG count")
    check(len(audio_files) == assets["audio_track_count"], "Runtime audio count")
    check(not assets["catalog_complete"] and not assets["full_content_data_complete"] and bool(assets["pending_categories"]), "Incomplete project falsely marked complete")
    result = {"planning_check": "fail" if errors else "pass", "species_slots": 156, "known_production_cards": len(species), "main_regions": len(main_regions), "postgame_regions": len(post_regions), "representatives": len(reps), "music_cues_not_generated": len(cues), "queued_assets_not_created": sum(q["state"] == "not_created" for q in queue), "runtime_image_count": len(runtime_pngs), "runtime_ready_images": len(ready_pngs), "errors": errors, "scope": "planning counts and references, not playthrough or complete content"}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
