from pathlib import Path
import argparse
import hashlib
import json
import struct

def main():
    parser = argparse.ArgumentParser(description='Check recorded files; this does not validate artwork quality or game completion.')
    parser.add_argument('--require-complete', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / 'manifests/assets.json').read_text(encoding='utf-8'))
    errors = []
    seen = set()
    for item in manifest['entries']:
        if item['id'] in seen:
            errors.append('Duplicate ID: ' + item['id'])
        seen.add(item['id'])
        path = (root / item['path']).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            errors.append('Missing or invalid path: ' + item['path'])
            continue
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != item['sha256']:
            errors.append('Hash mismatch: ' + item['path'])
        if path.suffix.lower() == '.png':
            if len(raw) < 33 or raw[:8] != b'\x89PNG\r\n\x1a\n' or raw[12:16] != b'IHDR':
                errors.append('Invalid PNG header: ' + item['path'])
                continue
            width, height = struct.unpack('>II', raw[16:24])
            if (width, height) != (item['png_width'], item['png_height']):
                errors.append('PNG dimensions changed: ' + item['path'])
    if args.require_complete and (not manifest['catalog_complete'] or not manifest['full_content_data_complete'] or manifest['pending_categories']):
        errors.append('Full asset/content preparation is not complete.')
    print(json.dumps({'recorded_file_check': 'pass' if not errors else 'fail', 'files_checked': len(seen), 'catalog_complete': manifest['catalog_complete'], 'runtime_images': manifest['runtime_image_count'], 'audio_tracks': manifest['audio_track_count'], 'pending_categories': manifest['pending_categories'], 'errors': errors, 'scope': 'file existence, hashes and PNG header dimensions only'}, ensure_ascii=False, indent=2))
    return 1 if errors else 0

if __name__ == '__main__':
    raise SystemExit(main())
