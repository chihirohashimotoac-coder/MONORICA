"""Recheck s01 candidates/preserved originals from commit-pinned GitHub bodies."""
import concurrent.futures
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import urllib.request
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
REPORT = ROOT / 'reports/art-parallel-20261104/s01'
BASE = 'b6c1d875e3f624bb77d1e632bfed561380d7ed19'
PIN = sys.argv[1]
M = json.loads((REPORT / 'manifest.json').read_text())
P = json.loads((REPORT / 'preservation-status.json').read_text())
EXPECTED = [f'wild_{x}_02' for x in ['seed_squirrel','vine_mole','breeze_bird','stream_otter','coil_dormouse','dusk_glider']]
EXPECTED += [f'wild_{family}_{stage:02}' for family,n in [('reed_crane',3),('lock_crab',3),('lotus_frog',2),('silt_skate',2),('mist_snail',2),('lantern_jelly',2),('bog_leech',2),('reed_whistle',1),('bubble_moth',1),('kiln_pup',3),('glass_gecko',3)] for stage in range(1,n+1)]
assert len(EXPECTED) == len(set(EXPECTED)) == 30
assert [e['species_id'] for e in M['entries']] == EXPECTED

def check(e):
    path = e.get('actual_image_path') or e['preserved_path']
    local = (ROOT / path).read_bytes()
    remote = urllib.request.urlopen('https://raw.githubusercontent.com/chihirohashimotoac-coder/MONORICA/'+PIN+'/'+path, timeout=60).read()
    digest = hashlib.sha256(remote).hexdigest()
    assert remote == local and len(remote) == e['size_bytes'] and digest == e['sha256'], path
    im = Image.open(io.BytesIO(remote)); im.load()
    assert (im.width,im.height,im.mode) == (e['width'],e['height'],e['mode']), path
    if 'prompt_file' in e:
        assert (ROOT / e['prompt_file']).stat().st_size > 0
        assert e['status'] == '保存確認済み' and e['adoption_status'] == 'pending_user_review'
    return dict(species_id=e['species_id'],path=path,sha256=digest,size_bytes=len(remote),width=im.width,height=im.height,mode=im.mode,github_body_match=True)

preserved = P['github_existing_9'] + P['library_existing_6']
assert len(preserved) == 15
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
    results = list(pool.map(check, M['entries']+preserved))
assert len({r['sha256'] for r in results[:30]}) == 30
assert len({r['path'] for r in results[:30]}) == 30

baseline_paths = subprocess.check_output(['git','ls-tree','-r','--name-only',BASE],cwd=ROOT,text=True).splitlines()
changed = []
for path in baseline_paths:
    before = subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
    if not (ROOT/path).is_file() or (ROOT/path).read_bytes() != before:
        changed.append(path)
assert not changed, changed
report = dict(date_jst='2026-11-05',reference_commit=BASE,readback_commit=PIN,assigned=30,saved_verified=30,incomplete=0,preserved_verified=15,unique_selected_candidate_hashes=30,baseline_file_count=len(baseline_paths),baseline_files_unchanged=True,selected_candidates=results[:30],preserved_originals=results[30:],visual_scope='27種は前工程の目視記録を保持。今回追加3種は生成本体と保存本体を目視。全45本体を今回HTTPS取得し実測・照合。美術採用やruntime昇格を意味しない。')
(REPORT/'completion-verification-20261105.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if not isinstance(v,list)},ensure_ascii=False))
