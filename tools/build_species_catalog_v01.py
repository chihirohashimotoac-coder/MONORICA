"""設計表の書き出し。ゲーム本体・数値バランス・画像は作らない。"""
from pathlib import Path
import collections
import copy
import csv
import hashlib
import json
import sys

from species_drafts_v01 import FAMILIES

ROOT = Path(__file__).resolve().parents[1]
VERSION = '0.1'
def read(n):
    return json.loads((ROOT / n).read_text(encoding='utf-8'))
def write(n, obj):
    p = ROOT / n
    p.parent.mkdir(parents=True, exist_ok=True)
    newline='\r\n' if p.is_file() and b'\r\n' in p.read_bytes() else '\n'
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8',newline=newline)
def md(n, text):
    p=ROOT/n
    newline='\r\n' if p.is_file() and b'\r\n' in p.read_bytes() else '\n'
    p.write_text(text.rstrip() + '\n', encoding='utf-8',newline=newline)

WORLD = read('content/planning/world-outline.json')
KNOWN = {s['id']: s for s in read('content/planning/known-species.json')['species']}
CHART = read('content/type-chart.json')
ASSETS = {a['id']: a for a in read('manifests/assets.json')['entries']}
REGIONS = {r['id']: r for r in WORLD['regions']}
TYPE_LABEL = {t['id']: t['label_ja'] for t in CHART['types']}
RANKS = {r['id']: (10 * (i+1) if i < 8 else 100) for i, r in enumerate(WORLD['regions'])}
RANKS['region_kazami'] = 11
FIELD = {
 'field_vine': {'name_ja':'つたうち', 'type_id':'grass', 'learn_rank':12, 'gate_rank':13,
  'region_id':'region_kazami', 'teacher':'森の入口の徒歩の講習場所', 'gate':'森の崖の支点',
  'battle':'草の攻撃と速さを下げる追加効果の案', 'primary_provider':'wild_vine_mole_01', 'required_gate_ids':[]},
 'field_wave': {'name_ja':'なみわたり', 'type_id':'water', 'learn_rank':21, 'gate_rank':22,
  'region_id':'region_minase', 'teacher':'水門手前の徒歩の船着場の講習', 'gate':'水郷の指定の岸から渡る水路',
  'battle':'水の攻撃。2対2では複数相手への攻撃候補', 'primary_provider':'wild_stream_otter_01', 'required_gate_ids':[]},
 'field_break': {'name_ja':'いわくだき', 'type_id':'earth', 'learn_rank':31, 'gate_rank':32,
  'region_id':'region_hinowa', 'teacher':'地熱洞手前の徒歩の工房講習', 'gate':'地熱洞のひび岩',
  'battle':'地の攻撃と防御を下げる追加効果の案', 'primary_provider':'wild_vine_mole_01', 'required_gate_ids':[]},
 'field_ember': {'name_ja':'ともしび', 'type_id':'fire', 'learn_rank':33, 'gate_rank':34,
  'region_id':'region_hinowa', 'teacher':'岩の講習後の徒歩の灯火広場', 'gate':'地熱洞奥の灯火',
  'battle':'炎の攻撃とやけどの追加効果の案', 'primary_provider':'wild_kiln_pup_01', 'required_gate_ids':['field_break']},
}

# hp・物攻・物防・特攻・特防・速さ。数値ではなく同段階の中での相対傾向。
ROLES = {
 'swift_special': ('速い特殊攻撃と立て直し', ('控えめ','控えめ','控えめ','高め','標準','高め'), '速さと特殊攻撃で先に仕事をする', '重い物理の一撃や先手を奪う妨害に弱い'),
 'breaker': ('攻撃による突破', ('標準','高め','標準','高め','控えめ','標準'), '有利な相手へ強く攻める', '大技後の隙と交代の読みを必要とする'),
 'counter_tank': ('耐久と物理反撃', ('高め','高め','高め','控えめ','標準','控えめ'), '受けた後に物理で押し返す', '補助による崩しと遅い行動順に弱い'),
 'allround': ('扱いやすい攻撃と補佐', ('標準','標準','標準','標準','標準','標準'), '攻撃と補助を無理なく選べる', '専門の突破役や壁ほどの強みはない'),
 'physical_wall': ('物理受け', ('高め','標準','高め','控えめ','控えめ','控えめ'), '物理を受けて交代と反撃の余地を作る', '特殊の集中攻撃と継続的な妨害が苦手'),
 'pivot': ('速い交代と対面調整', ('標準','標準','控えめ','標準','控えめ','高め'), '先に動いて有利な仲間へつなぐ', '受け続ける耐久や単独の大火力は控えめ'),
 'physical_attacker': ('物理攻撃', ('標準','高め','標準','控えめ','控えめ','標準'), '物理技の選択で攻撃範囲を作る', '物理の壁や攻撃を下げる妨害が苦手'),
 'disruptor': ('行動順・手順の妨害', ('標準','控えめ','標準','標準','標準','高め'), '相手の決まった勝ち筋をずらす', '妨害だけでは決め切れず、強い直接攻撃に押される'),
 'healer': ('攻撃できる回復補佐', ('標準','控えめ','標準','標準','高め','標準'), '攻撃を残しつつ味方や自分を立て直す', '回復を妨げる圧力と重い物理攻撃が苦手'),
 'special_wall': ('特殊受け', ('高め','控えめ','控えめ','標準','高め','控えめ'), '特殊攻撃を受けて味方へつなぐ', '強い物理攻撃と継続的な補助妨害が苦手'),
 'special_attacker': ('特殊攻撃', ('標準','控えめ','控えめ','高め','標準','標準'), '物理の壁を特殊で攻める', '物理の速攻や特殊の壁が苦手'),
 'attrition': ('持続圧と削り', ('高め','控えめ','標準','標準','高め','控えめ'), '回復を挟み少しずつ有利を作る', '短期の決定力と状態変化への対策を持つ相手が苦手'),
 'double_support': ('2対2の連携補佐', ('標準','控えめ','標準','標準','高め','標準'), '味方の順序や立て直しを助ける', '単独の突破力は控えめ。1対1用の攻撃も残す'),
}
ANATOMY_KEYS = ['independent_arms','legs','independent_wings','tails','horns','antennae','fins','tentacles']
TIME_JA = {'all':'昼夜共通','day':'ゲーム内の昼','night':'ゲーム内の夜','evening':'ゲーム内の夕方'}
RARITY_JA = {'common':'よく見かける','uncommon':'やや少ない','rare':'珍しい','gift':'保護・譲渡イベント','fixed_repeatable':'再挑戦できる固定希少種'}
SPECIAL_ID = {'starter_flower_hare': 'ハルネ研究所', 'starter_ember_wyvern': 'ハルネ研究所', 'starter_tide_bear': 'ハルネ研究所'}

def normalized(fid):
    return fid if fid.startswith(('starter_', 'wild_')) else 'wild_' + fid

def evolution_condition(f, i):
    if i >= len(f['stages'])-1:
        return None
    value = f['evolve'][i]
    if isinstance(value, int):
        return {'method':'level','level':value,'status':'confirmed' if f['region']=='starter' else 'production_proposal',
                'text_ja':f'Lv{value}以上でレベルアップ。延期した場合は次のレベルアップで再判定。','unlock_story_rank':0}
    x = copy.deepcopy(value)
    x['text_ja'] = x.pop('text')
    x['status'] = 'production_proposal'
    x['unlock_story_rank'] = x.pop('rank',0)
    return x

def matchup(types):
    out = {}
    for attacker in CHART['type_order']:
        v = 1
        for defender in types:
            v *= CHART['damage_multipliers'][attacker][defender]
        out[attacker] = v
    return out

def proposals(old, effective):
    if not old:
        return [{'field':'entire_record','status':'production_proposal','reason_ja':'今回新規の種。ユーザー採用済みではない。'}]
    result = [{'field':'new_detail_fields','status':'production_proposal','reason_ja':'数値以外の技・生態・入手・補完構造は今回の制作案。既存カードを上書きしない。'}]
    if old['evolves_to'] != effective['evolves_to']:
        # 確認済み御三家の関係は値を維持。追加の表示メタデータとの差は変更案にしない。
        a,b = old['evolves_to'],effective['evolves_to']
        if not a and b:
            result.append({'field':'evolves_to','previous':None,'proposed':b,'status':'production_proposal',
                           'reason_ja':'既存カードは進化先未確定。世界骨格の2段階案を設計表側に接続。'})
    if old.get('secondary_type_candidate') != effective['secondary_type']:
        result.append({'field':'secondary_type','previous':old.get('secondary_type_candidate'),
                       'proposed':effective['secondary_type'],'status':'production_proposal'})
    return result

def art_state(sid, old, f, i):
    # 採用範囲を分解し、古いモデル制作文書より現在のカード・Handoffを優先する。
    if old:
        direction = old['design_status']
        model = old.get('model_sheet_status','not_created_as_individual_sheet')
        runtime = old['runtime_art_status']
        if sid=='starter_flower_hare_01':
            model='direction_adopted_back_orientation_corrected'
        unseen = '既存原画・設定画で確認できない接続、最終形の背面、今回の補完は制作案。'
        if sid in ['wild_stream_otter_01','wild_coil_dormouse_01','wild_dusk_glider_01']:
            unseen='比較原画の造形方向は採用済み。新設定画の背面・横面・接続は確認待ち。'
        return dict(concept_direction=direction, model_sheet=model, runtime_art=runtime,
                    new_anatomy_detail='production_proposal_unless_explicit_inherited_constraint',
                    note_ja=unseen)
    return dict(concept_direction='production_proposal',model_sheet='not_created',runtime_art='not_created',
                new_anatomy_detail='production_proposal',note_ja='今回の文字設計のみ。画像未制作・未採用。')

def references(old):
    refs = ['docs/SPECIES_ALLOCATION_v0.1.md','docs/WORLD_OUTLINE_v0.1.md',
            'content/planning/world-outline.json','content/type-chart.json','tools/species_drafts_v01.py']
    asset_ids=[]
    if old:
        refs += ['content/planning/known-species.json','docs/DECISIONS.md','HANDOFF_MONORICA_2026-11-02_v0.12.md']
        for k in ['reference_asset_id','model_sheet_asset_id']:
            if old.get(k): asset_ids.append(old[k])
        asset_ids += old.get('runtime_asset_ids',old.get('runtime_candidate_asset_ids',[]))
        for aid in asset_ids:
            refs.append(ASSETS[aid]['path'])
    return list(dict.fromkeys(refs)),asset_ids

def build():
    species=[]
    families=[]
    for f in FAMILIES:
        fid=normalized(f['id'])
        ids=[fid+'_'+str(i+1).zfill(2) for i in range(len(f['stages']))]
        isstarter=f['region']=='starter'
        base_rank=10 if isstarter else (14 if fid=='wild_dusk_glider' else RANKS[f['region']])
        earliest=base_rank
        parent_condition=None
        family_species=[]
        for i,s in enumerate(f['stages']):
            sid=ids[i]
            old=KNOWN.get(sid)
            typ=s['types']
            d=matchup(typ)
            next_cond=evolution_condition(f,i)
            nxt=None if next_cond is None else dict(id=ids[i+1], **next_cond)
            origin_region='region_kazami' if isstarter else f['region']
            time=f['time']
            rare=f['rarity']
            if i>0:
                earliest=max(earliest,parent_condition['unlock_story_rank'])
                acq=[dict(method='evolution',source_species_id=ids[i-1],condition=copy.deepcopy(parent_condition),
                    region_id=None,story_rank=earliest,required_field_move_ids=[],solo=True,repeatable=True,
                    encounter_time=None,external_requirement=False,
                    text_ja=f"{f['stages'][i-1]['name']}から進化：{parent_condition['text_ja']}")]
                first=f"進化元を入手した後、{parent_condition['text_ja']}"
                wild_locations=[]
                rarity='evolution_only'
                condition_ja='野生出現なし。進化条件を参照。'
            elif isstarter:
                acq=[dict(method='starter_choice',region_id='region_kazami',story_rank=10,choice_family_id=fid,
                         required_field_move_ids=[],solo=True,repeatable=False,external_requirement=False,
                         encounter_time='all',text_ja='序章の研究所で3系列から選ぶ。'),
                     dict(method='postgame_rescue',region_id='post_shizuna',story_rank=100,
                         required_field_move_ids=[],solo=True,repeatable=True,external_requirement=False,
                         encounter_time='all',text_ja='本編クリア後、徒歩のシズナ保護施設で系列別の観察・保護イベント。選ばなかった2系列の両方を取得でき、二者択一にしない。')]
                first='選んだ系列は序章。選ばなかった系列は本編クリア後のシズナ保護イベント。'
                wild_locations=[]
                rarity='gift'
                condition_ja='昼夜共通。本編中の他の2系列取得は不可。'
            else:
                method='fixed_repeatable' if rare=='fixed_repeatable' else 'wild_capture'
                acq=[dict(method=method,region_id=f['region'],story_rank=base_rank,required_field_move_ids=list(f['acquire_gates']),
                    solo=True,repeatable=True,external_requirement=False,encounter_time=time,
                    text_ja=('徒歩の固定観察場所で捕獲戦。敗北・逃走・撃破後も安全地点へ戻れば再挑戦。捕獲後も保護調査の再遭遇で再入手できる制作案。'
                             if method=='fixed_repeatable' else '徒歩で到達する生息地で繰り返し捕獲。捕獲道具は通常店・講習の再補充から取得。'))]
                first=REGIONS[f['region']]['name_ja']+'到達後。'+TIME_JA[time]+'。'
                if fid=='wild_dusk_glider':
                    first='森のつた支点開通後。通常はゲーム内の夜。昼の異変固定個体は唯一の入手経路にしない。'
                wild_locations=[] if method=='fixed_repeatable' else [dict(region_id=f['region'],environment_ja=f['ecology'],access='on_foot_after_required_gates' if f['acquire_gates'] else 'on_foot_before_local_required_gate')]
                rarity=rare
                condition_ja=TIME_JA[time]+'。天候・現実日付・期間限定条件なし。'
            role_id=s.get('role',f['role'])
            role,statvals,strong,weak=ROLES[role_id]
            learn=[]
            for mid in f['field']:
                mv=FIELD[mid]
                learn.append(dict(move_id=mid,name_ja=mv['name_ja'],method='reusable_free_lesson',
                    unlock_story_rank=mv['learn_rank'],teacher_region_id=mv['region_id'],required_gate_ids=list(mv['required_gate_ids']),status='production_proposal',
                    text_ja=mv['teacher']+'。無償・再受講可。進化後も再習得でき、4技から1つ入れ替える。'))
            move_name,move_effect=s['move'].split('|',1)
            move_id='draft_'+sid+'_signature'
            anatomy=dict(zip(ANATOMY_KEYS,s.get('anatomy',f['anatomy'])))
            connection=s.get('connection',f['connection'])
            refs,asset_ids=references(old)
            effective=dict(dex_number=len(species)+1,id=sid,name_ja=s['name'],family_id=fid,
                evolution_stage=i+1,family_stage_count=len(ids),evolves_from=ids[i-1] if i else None,
                evolves_to=nxt,evolution_condition_from=copy.deepcopy(parent_condition),
                primary_type=typ[0],secondary_type=typ[1] if len(typ)>1 else None,
                allocation_bucket_id='starter_pool' if isstarter else f['region'],
                allocation_region_id=None if isstarter else f['region'],
                battle=dict(role_id=role_id,role_ja=role,ability_trends=dict(zip(['hp','attack','defense','special_attack','special_defense','speed'],statvals)),
                    ability_trends_scope='同じ進化段階内の相対的な制作案。具体的種族値ではない。',
                    strengths_ja=strong+'。'+s['tactic'],weaknesses_ja=weak,
                    received_type_multipliers=d,weak_to_type_ids=[t for t,v in d.items() if v>1],
                    resists_type_ids=[t for t,v in d.items() if 0<v<1],immune_type_ids=[t for t,v in d.items() if v==0],
                    damage_basis='content/type-chart.json。防御側複合は積。特性・道具・場・能力値は含めない。',
                    move_direction_ja=s['tactic'],signature_move=dict(id=move_id,name_ja=move_name,effect_ja=move_effect,
                        type_candidates=typ, power=None,accuracy=None,usage_count=None,status='production_proposal',
                        note_ja='数値・対象・発動順の詳細は未検証。'),numeric_stats_status='not_designed'),
                exploration=dict(role_ja=('／'.join(FIELD[m]['name_ja'] for m in f['field'])+'の習得候補。実際に覚えた個体を手持ちへ。' if learn else '必須探索技の担当なし。生態の観察と任意の発見を担う。'),
                    field_move_ids=list(f['field']),learn_methods=learn,battle_slots_used_per_move=1,
                    requires_currently_learned_move=True,requires_in_party=True,status='production_proposal_with_confirmed_four_slot_rule'),
                habitat=dict(primary_region_id=origin_region,environment_ja=f['ecology'],ecology_ja=f['ecology'],
                    environment_status='production_proposal',wild_locations=wild_locations,
                    note_ja='進化のみの種の地域は系列の生態・制作配分であり、野生出現場所を意味しない。' if i else ('相棒は野生出現を設定せず研究所と保護イベントで取得。' if isstarter else '生息場所は制作案。実マップの接続は未検証。')),
                acquisition=dict(first_available_ja=first,earliest_story_rank=earliest,methods=acq,
                    rarity=rarity,rarity_ja='進化のみ（野生出現なし）' if i else RARITY_JA[rare],
                    appearance_conditions_ja=condition_ja,phase='choice_dependent_main_and_postgame' if isstarter else REGIONS[f['region']]['phase'],
                    repeatable_source_ja='進化元の通常再入手・再育成から繰り返せる。' if i else ('本編クリア後の保護調査で再取得できる制作案。' if isstarter else '通常捕獲または固定調査の再挑戦。'),
                    acquisition_status='production_proposal',no_external_requirements=True),
                art=dict(motifs_ja=f['motif'],full_body_silhouette_ja=s['silhouette'],palette_main=f['palette'][:2],palette_accents=f['palette'][2:],
                    palette_status='retain_existing_palette_direction' if old else 'production_proposal',
                    face_expression_ja=f['face'],anatomy_counts=anatomy,anatomy_connections_ja=connection,
                    anatomy_scope_ja='数と接続は原画で確認できる部分を維持。未確認部分は制作案。' if old else '全構造が今回の制作案。未制作の画像で確認済みとは扱わない。',
                    view_invariants=dict(front_ja='顔・前側の色面：'+f['face']+' 識別点：'+s['mark'],
                        back_ja='背面でも保つ輪郭：'+s['silhouette']+'。'+connection,
                        side_ja='横面の接続：'+connection+'。'+s['change']),
                    evolution_changes_ja=s['change'],family_retained_features_ja=f['motif']+'。'+f['face'],
                    sprite_96px_ja=s['silhouette']+'。'+s['mark']+'を太い色面で残し、細い陰影より器官の重なりを優先。',
                    icon_32px_ja=s.get('icon',s['mark']+'を最優先。細部を省略しても付け根と本数の設計は変えない。'),
                    differentiation_ja=f['contrast'],production_difficulty_ja=f['notes'],
                    art_adoption=art_state(sid,old,f,i)),
                provenance=dict(origin='existing_with_proposed_details' if old else 'new_production_proposal',
                    name_status=old['name_status'] if old else 'production_proposal',
                    typing_status=old['type_status'] if old else 'production_proposal',
                    original_concept_status=old['design_status'] if old else 'production_proposal',
                    game_design_status='proposal_with_inherited_decisions' if old else 'production_proposal',
                    confirmed_inherited_fields=['evolves_to.level','starter_selection_policy','battle.role_direction'] if isstarter else [],
                    source_paths=refs,source_asset_ids=asset_ids,legacy_card_snapshot=copy.deepcopy(old),
                    new_fields_status='production_proposal',user_adopted_new_design=False))
            effective['provenance']['change_proposals']=proposals(old,effective)
            if sid.startswith('starter_ember_wyvern'):
                effective['art']['explicit_anatomy_constraint']={'status':'user_adopted_for_family','independent_arms':2,'legs':2,'independent_wings':2,'wing_forelimbs':False}
            if sid.startswith('wild_dusk_glider'):
                effective['art']['explicit_anatomy_constraint']={'status':'current_user_requirement','legs':4,'independent_wings':0,'membrane_pairs':1,'connection_ja':'手首から足首、四肢4本のみ。'}
            species.append(effective)
            family_species.append(sid)
            parent_condition=next_cond
        families.append(dict(id=fid,allocation_bucket_id='starter_pool' if isstarter else f['region'],species_ids=family_species,
             stage_count=len(ids),motif_ja=f['motif'],status='production_proposal_with_preserved_existing_constraints'))
    # 量産前の配分と個々の設計は別データとして見渡せるようにする。
    dist={}
    for r in WORLD['regions']:
        dist[r['id']]={'name_ja':r['name_ja'],'original_slots':r['new_species_slots'],'proposed_slots':r['new_species_slots'],
                       'actual_count':sum(s['allocation_region_id']==r['id'] for s in species),'changed':False}
    cat=dict(schema_version=VERSION,purpose='planning_only_not_runtime',status='complete_156_entry_design_draft_not_user_adopted',
        design_draft_complete=True,approved_game_data_complete=False,art_complete=False,
        created_date_jst='2026-11-02',source_bundle='MONORICA_preproduction_v0.12.zip',
        policy_ja=['今回の156種は詳細設計の制作案。採用済み美術・既存進化条件を継承する範囲と分ける。',
                   '図鑑番号はこの版で固定する制作番号。種IDは改名・並べ替えで変更しない。',
                   '進化は別種、色違い・雌雄・姿勢・美術版違いは種数へ加算しない。',
                   '進化後の初入手は親の取得と条件達成後。レベルと地域の強制的な結び付けを設けない。',
                   '相性は試作用の表から計算。数値バランス・捕獲・全編通しプレイは未検証。'],
        types=[dict(t) for t in CHART['types']],regions=copy.deepcopy(WORLD['regions']),
        allocation=dict(starter_pool=9,regions=dist,total=156,changes=[]),
        role_definitions=[dict(id=k,name_ja=v[0],strength_ja=v[2],weakness_ja=v[3]) for k,v in ROLES.items()],
        field_moves=[dict(id=k,**v,status='production_proposal',source_path='brief/11_field_moves_and_opening_v0.2.md',
            slot_rule='対応技が現在の戦闘4枠にあり、その個体が手持ちにいる。',
            relearn_rule='無償・繰り返し講習と回復施設の思い出し。進化で自動消去しない。',
            field_usage_rule_proposal='探索時は戦闘用使用回数を消費せず、0でも使用可。戦闘不能時は安全地で回復してから使用する案。') for k,v in FIELD.items()],
        time_policy=dict(status='production_proposal',clock='game_internal',advance='安全地点で無償待機し昼・夕・夜を選べる。現実時刻・日付へ依存しない。'),
        return_safety_policy=dict(status='production_proposal',rules_ja=[
            'つた・岩の仕掛けは帰路の開通を保持する。','水上と水路で隔てられた岸で、最後のなみわたりを失う忘却・預け入れ・逃がす操作を不可にする。',
            '技のない個体や預かりからの遠隔探索は許可しない。','非常帰還は到達済み入口のみ。未開通の先へ進む代替手段にしない。',
            '回復施設で必要な通常種の再捕獲と無償再習得へ戻れる。','複数の探索技を要する必須区間は最大2種類を目標とする。実マップ未制作。',
            '灯火は帰路に必要な状態を保存する。中断再開後も帰路の岩・つた・灯火の開通状態と到達済み入口を復元する。',
            '孤立した岸・全手持ち戦闘不能・技忘却・手持ち変更後は、到達済みの安全な入口へ非常帰還できる案。帰還先を保存し、そこから回復施設へ徒歩で戻れる配置にする。']),
        evolution_sites=[
            dict(id='site_glass_kiln',name_ja='ヒノワ旧窯観察台',region_id='region_hinowa',unlock_story_rank=35,access_required_gate_ids=['field_ember'],
                 repeatable=True,consumable_required=False,status='production_proposal',access_ja='灯火通路開通後の徒歩の旧窯。調べる操作で進化し、何度でも再取得可。'),
            dict(id='site_memory_ring',name_ja='メグリ古観測環',region_id='post_meguri',unlock_story_rank=102,access_required_gate_ids=[],
                 repeatable=True,consumable_required=False,status='production_proposal',access_ja='牧場から徒歩で行ける観測環。有限の道具や図鑑全収集を要求しない。'),
            dict(id='site_frost_pool',name_ja='メグリ地下湖岸の冷水台',region_id='post_meguri',unlock_story_rank=101,access_required_gate_ids=[],
                 repeatable=True,consumable_required=False,status='production_proposal',access_ja='徒歩の地下湖岸。水上移動や進化後の個体を入場条件にしない。')],
        families=families,species=species,
        unresolved_ja=['新規141種と既存15種への詳細追加はユーザー未採用。一般6種の表示名・属性と追加進化6種も案。',
            'ミズッタv0.1・ココイルv0.1・ヨルミルv0.2の新三面設定画は確認待ち。',
            '御三家中間形の美術は提案、最終形は方向採用のみで背面接続の新設計は未採用。',
            '進化レベル（御三家以外）・場所進化・技名と具体効果・昼夜待機・再挑戦は制作案。',
            '種族値・技威力・命中・技使用回数・成長曲線・捕獲率・出現率・実マップ・ゲーム内UIは未設計または未検証。',
            '固有名と造形の網羅的な既存作品照合・商標調査は未実施。独自モチーフの組合せと輪郭を設計したが法的保証ではない。'])
    write('content/planning/species-catalog_v0.1.json',cat)
    return cat

def type_text(s):
    return '・'.join(TYPE_LABEL[t] for t in [s['primary_type'],s['secondary_type']] if t)

def region_text(s):
    return '御三家別枠' if not s['allocation_region_id'] else REGIONS[s['allocation_region_id']]['name_ja']

def evo_text(s):
    return s['evolution_condition_from']['text_ja'] if s['evolution_condition_from'] else ('単独種' if s['family_stage_count']==1 else '基礎形')

def write_tables(cat):
    byid={s['id']:s for s in cat['species']}
    all_s=cat['species']
    counts=collections.Counter(s['primary_type'] for s in all_s)
    secondary=collections.Counter(s['secondary_type'] for s in all_s if s['secondary_type'])
    roles=collections.Counter(s['battle']['role_id'] for s in all_s)
    lines=['# MONORICA 全156種設計表 v0.1','',
      '2026-11-02作成、2026-11-04設計レビュー反映（日本時間）。全156種を記述した**制作案**。既存15種のID・名前・確定した御三家進化条件を維持し、141種を追加。採用済み原画と文字設計案の状態は各カードを参照。レビュー記録は[SPECIES_REVIEW_v0.1.md](SPECIES_REVIEW_v0.1.md)。','',
      '詳細は [全種詳細](SPECIES_DESIGN_DETAILS_v0.1.md)、[JSON](../content/planning/species-catalog_v0.1.json)、[CSV](../content/planning/species-catalog_v0.1.csv)、[共通スキーマ](../content/planning/species-catalog_v0.1.schema.json)。','',
      '## 配分と数え方','',
      '御三家9＋カザミ12＋ミナセ18＋ヒノワ18＋カナト18＋ツキシロ18＋サナギ18＋アカツキ15＋ホシミ12＋シズナ9＋メグリ9＝156。元の地域配分から変更なし。各進化形は1種、色・性別・姿勢差分は加算しない。','',
      '79系列：3段階17系列（51種）、2段階43系列（86種）、単独19種。一般6系列の進化先名は既存世界骨格の案を引き継いだ。残る135種を新しく設計した。','',
      '配分地域は系列の制作枠であり、進化後の野生出現場所ではない。本編中に1人が取得できる設計上の種数は132（一般129＋選んだ御三家3）。クリア後に24種（新地域18＋他の御三家6）が加わり156。育成レベルの到達時期・所要時間は未測定。','',
      '地域・系列・生態の方針は [配分方針](SPECIES_ALLOCATION_v0.1.md) に記録。地域名・人物名は元資料でも提案段階のまま。','',
      '| 属性 | 主属性 | 副属性 | 合計登場枠 |','|---|---:|---:|---:|']
    for t in CHART['type_order']:
        lines.append(f"| {TYPE_LABEL[t]} | {counts[t]} | {secondary[t]} | {counts[t]+secondary[t]} |")
    lines += ['', '複合種は属性登場枠に2回数える。種数156とは別の集計。主属性は9〜16種で、単独属性と複合属性を混ぜた。御三家の最終複合属性は未決定のため、この版では元の単属性候補を保持。','',
      '| 戦闘役割 | 種数 |','|---|---:|']
    for rid,v in ROLES.items(): lines.append(f'| {v[0]} | {roles[rid]} |')
    lines += ['', '役割は系列の主軸を基本とし、カワミオは速い交代、マユシラは繭の特殊受けへ変化する制作案。具体的な種族値・技威力・最終的な強さは未設定。比較可能な相性倍率は既存表から計算し、特性や道具は含めない。','',
      '## 探索と入手の設計','',
      '序盤に草のツルモグ、水のミズッタ、雷のココイル、風のハネリを通常捕獲でき、御三家の選択を補う。12属性の基礎形はヒノワ到達までに全て通常種から取得可能な制作案。','',
      '| 必須技の案 | 通常種の主な提供元 | 最初の講習 | 必要地点 |','|---|---|---|---|']
    for mid,m in FIELD.items():
        lines.append(f"| {m['name_ja']} | {byid[m['primary_provider']]['name_ja']} | {m['teacher']} | {m['gate']} |")
    lines += ['', '全技が戦闘4枠の1枠を使う。習得済みの個体を手持ちに入れる。講習は無償・再受講可、進化後も再習得可という制作案。思い出し・使用回数0時・帰路・水上での忘却防止は設計上の方針であり、実装や通しプレイで保証したものではない。','',
      '夜行種と夕方種はゲーム内の安全地点で無償待機できる案。現実の日時、通信交換、対人、配布、課金、外部サービスは入手に不要。固定希少種は再挑戦できる。','',
      '## 採用状態の読み方','',
      '- **既存＋案**：既存種を継承し、生態・技・進化先などの詳細を今回提案。既存の全仕様が確定した意味ではない。',
      '- **制作案**：追加141種。うち一般進化6種の名前・方向は既存の世界骨格にある案。採用済みとはしない。',
      '- **静止素材採用**：御三家初期3体とリスコロ・ツルモグ・ハネリの各3PNG。UIを含むruntime PNG19枚は変更なし。',
      '- **新設定画確認待ち**：ミズッタv0.1・ココイルv0.1・ヨルミルv0.2。ヨルミル旧v0.1は不採用で参照対象にしない。',
      '- 御三家の名前は委任された作業名、一般6種の名前・属性は提案の状態を保持。中間形の美術は提案、最終形は造形方向のみ採用。','',
      '## 図鑑一覧','',
      '| No. | 名前 | 系列・段階 | 属性案 | 配分枠 | 役割 | 最初の入手 | 出自 |','|---:|---|---|---|---|---|---|---|']
    for s in all_s:
        base=next(f for f in cat['families'] if f['id']==s['family_id'])['species_ids'][0]
        how='進化のみ：'+evo_text(s) if s['evolves_from'] else s['acquisition']['first_available_ja']
        lines.append(f"| {s['dex_number']:03} | {s['name_ja']} | {byid[base]['name_ja']} {s['evolution_stage']}/{s['family_stage_count']} | {type_text(s)} | {region_text(s)} | {s['battle']['role_ja']} | {how} | {'既存＋案' if s['id'] in KNOWN else '制作案'} |")
    lines += ['', '## 残る確認','']+[f'- {x}' for x in cat['unresolved_ja']]
    lines += ['', '検査結果は [整合性レポート](../reports/species-catalog-check_v0.1.json) を参照。構造と参照の成功は、ゲームバランス・面白さ・実機の検証済みを意味しない。']
    md('docs/SPECIES_CATALOG_v0.1.md','\n'.join(lines))
    headers=['図鑑番号','種ID','名前','系列ID','進化段階','系列段階数','進化元','進化先','進化条件','主属性','副属性','配分枠','生態地域','環境','初入手','方法','珍しさ','昼夜条件','区分','主な役割','能力傾向','得意','苦手','受け弱点倍率','受け耐性倍率','専用技案','技効果案','探索役','モチーフ','シルエット','主配色','差し色','顔','器官数','接続','前面識別','背面識別','横面識別','進化変化','引継点','96px','32px','差別化','制作難度','出自','名前状態','属性状態','ゲーム設計状態','美術方向状態','設定画状態','静止素材状態','構造補完状態','変更案','参照']
    with (ROOT/'content/planning/species-catalog_v0.1.csv').open('w',encoding='utf-8-sig',newline='') as out:
        writer=csv.DictWriter(out,fieldnames=headers)
        writer.writeheader()
        for s in all_s:
            b,a,p,q=s['battle'],s['art'],s['provenance'],s['acquisition']
            writer.writerow(dict(zip(headers,[s['dex_number'],s['id'],s['name_ja'],s['family_id'],s['evolution_stage'],s['family_stage_count'],s['evolves_from'] or '',(s['evolves_to'] or {}).get('id',''),evo_text(s),TYPE_LABEL[s['primary_type']],TYPE_LABEL.get(s['secondary_type'],''),region_text(s),REGIONS[s['habitat']['primary_region_id']]['name_ja'],s['habitat']['environment_ja'],q['first_available_ja'],'／'.join(x['text_ja'] for x in q['methods']),q['rarity_ja'],q['appearance_conditions_ja'],q['phase'],b['role_ja'],'／'.join(k+':'+v for k,v in b['ability_trends'].items()),b['strengths_ja'],b['weaknesses_ja'],'／'.join(TYPE_LABEL[t]+f'×{b["received_type_multipliers"][t]:g}' for t in b['weak_to_type_ids']),'／'.join(TYPE_LABEL[t]+f'×{b["received_type_multipliers"][t]:g}' for t in b['resists_type_ids']+b['immune_type_ids']),b['signature_move']['name_ja'],b['signature_move']['effect_ja'],s['exploration']['role_ja'],a['motifs_ja'],a['full_body_silhouette_ja'],'／'.join(a['palette_main']),'／'.join(a['palette_accents']),a['face_expression_ja'],json.dumps(a['anatomy_counts'],ensure_ascii=False),a['anatomy_connections_ja'],a['view_invariants']['front_ja'],a['view_invariants']['back_ja'],a['view_invariants']['side_ja'],a['evolution_changes_ja'],a['family_retained_features_ja'],a['sprite_96px_ja'],a['icon_32px_ja'],a['differentiation_ja'],a['production_difficulty_ja'],p['origin'],p['name_status'],p['typing_status'],p['game_design_status'],a['art_adoption']['concept_direction'],a['art_adoption']['model_sheet'],a['art_adoption']['runtime_art'],a['art_adoption']['new_anatomy_detail'],json.dumps(p['change_proposals'],ensure_ascii=False),'／'.join(p['source_paths'])])))
    details=['# 全156種の制作カード詳細 v0.1','','JSONと同じ制作案を日本語で確認するための文書。共通スキーマと機械参照はJSONを正とする。採用範囲は各種の末尾を参照。','']
    for s in all_s:
        b,a,p,q=s['battle'],s['art'],s['provenance'],s['acquisition']
        weak='、'.join(TYPE_LABEL[t]+f'×{b["received_type_multipliers"][t]:g}' for t in b['weak_to_type_ids']) or 'なし'
        res='、'.join(TYPE_LABEL[t]+f'×{b["received_type_multipliers"][t]:g}' for t in b['resists_type_ids']+b['immune_type_ids']) or 'なし'
        details += [f"## {s['dex_number']:03} {s['name_ja']}",'',
          f"`{s['id']}`／系列 `{s['family_id']}`／{s['evolution_stage']}/{s['family_stage_count']}段階／{type_text(s)}（属性案）",'',
          f"進化元：{byid[s['evolves_from']]['name_ja'] if s['evolves_from'] else 'なし'}。{evo_text(s)}。進化先：{byid[s['evolves_to']['id']]['name_ja'] if s['evolves_to'] else 'なし'}。",'',
          f"**戦闘**：{b['role_ja']}。{b['strengths_ja']} 苦手：{b['weaknesses_ja']}。能力傾向："+'、'.join(k+'='+v for k,v in b['ability_trends'].items())+'。数値は未設定。',
          f"受け相性：弱点 {weak}／耐性・無効 {res}。既存相性表のみの計算。",'',
          f"技案「{b['signature_move']['name_ja']}」：{b['signature_move']['effect_ja']}。威力・命中・使用回数は未設定。",'',
          f"**入手**：{q['first_available_ja']} 方法："+'／'.join(x['text_ja'] for x in q['methods'])+f"。{q['rarity_ja']}。{q['appearance_conditions_ja']}。",
          f"生態：{s['habitat']['environment_ja']} {s['habitat']['note_ja']}",
          f"探索：{s['exploration']['role_ja']}。",'',
          f"**外見**：{a['motifs_ja']}。{a['full_body_silhouette_ja']}。配色："+'／'.join(a['palette_main'])+'、差し色：'+'／'.join(a['palette_accents'])+'。',
          '顔：'+a['face_expression_ja'],'器官数：'+'、'.join(k+'='+str(v) for k,v in a['anatomy_counts'].items())+'。接続：'+a['anatomy_connections_ja'],
          '前面：'+a['view_invariants']['front_ja'],'背面：'+a['view_invariants']['back_ja'],'横面：'+a['view_invariants']['side_ja'],
          '進化変化：'+a['evolution_changes_ja'],'引継点：'+a['family_retained_features_ja'],
          '96px：'+a['sprite_96px_ja'],'32px：'+a['icon_32px_ja'],
          '差別化：'+a['differentiation_ja'],'制作難度・注意：'+a['production_difficulty_ja'],
          '構造の扱い：'+a['anatomy_scope_ja'], '',
          f"**状態**：出自={p['origin']}、名前={p['name_status']}、属性={p['typing_status']}、ゲーム設計={p['game_design_status']}。美術方向={a['art_adoption']['concept_direction']}、設定画={a['art_adoption']['model_sheet']}、静止素材={a['art_adoption']['runtime_art']}。{a['art_adoption']['note_ja']}",'',
          '参照：'+'、'.join('`'+x+'`' for x in p['source_paths']), '']
    md('docs/SPECIES_DESIGN_DETAILS_v0.1.md','\n'.join(details))

def write_batches(cat):
    byid={s['id']:s for s in cat['species']}
    adopted={s['id'] for s in cat['species'] if s['art']['art_adoption']['runtime_art']=='static_sprites_visual_adopted_technical_checked'}
    # 採用済み6体は参照に残す。新設定画対象150体を10〜15体、同系列を分割せず詰める。
    groups=[]
    for f in cat['families']:
        todo=[sid for sid in f['species_ids'] if sid not in adopted]
        if todo: groups.append((f,todo))
    cache={}
    def solve(i,k):
        if i==len(groups): return (0,[]) if k==0 else None
        if k==0: return None
        if (i,k) in cache:return cache[i,k]
        n=0;best=None
        for j in range(i,len(groups)):
            n+=len(groups[j][1])
            if n>15:break
            if n<10:continue
            tail=solve(j+1,k-1)
            if tail:
                candidate=((n-12.5)**2+tail[0],[(i,j+1)]+tail[1])
                if best is None or candidate[0]<best[0]:best=candidate
        cache[i,k]=best
        return best
    solution=solve(0,12)
    assert solution is not None
    batches=[]
    for n,(a,b) in enumerate(solution[1],1):
        selected=groups[a:b]
        ids=[sid for _,todo in selected for sid in todo]
        refs=[sid for f,_ in selected for sid in f['species_ids'] if sid in adopted]
        batches.append(dict(id=f'art_batch_{n:02}',species_ids=ids,reference_only_species_ids=refs,
            status='planned_not_started',new_or_pending_model_sheet_count=len(ids),
            shared_focus_ja='／'.join(dict.fromkeys(region_text(byid[sid]) for sid in ids))+'の配分枠。系列内の接続・配色をそろえる。',
            family_ids=[f['id'] for f,_ in selected]))
    write('content/planning/species-art-batches_v0.1.json',dict(status='production_proposal',reference_only_adopted_species=sorted(adopted),
          target_species_count=150,batches=batches))
    lines=['# 設定画制作バッチ案 v0.1','',
      '今回は順番の設計のみで、画像制作は未着手。採用済み6体は再制作せず参照照合に使う。未確定の三面設定150体を12バッチ、各10〜15体へまとめた。同系列の制作対象は分割していない。','',
      '採用済み参照6体：'+ '、'.join(byid[x]['name_ja'] for x in sorted(adopted))+'。既存19PNGと元原画は変更しない。','',
      'ミズッタv0.1・ココイルv0.1・ヨルミルv0.2は、該当バッチで既存候補の確認を先に行う。採用前の自動再生成や採用状態の変更をしない。御三家中間形は既存提案を照合し、最終形は採用原画の方向を維持しつつ未確認接続を別案として補う。','',
      '| バッチ | 対象数 | 対象 | 共通点・目的 |','|---|---:|---|---|']
    for b in batches:
        lines.append(f"| {b['id']} | {len(b['species_ids'])} | "+'、'.join(byid[x]['name_ja'] for x in b['species_ids'])+f" | {b['shared_focus_ja']} |")
    for b in batches:
        lines += ['',f"## {b['id']}：{len(b['species_ids'])}体",'',b['shared_focus_ja'],'',
             '採用済み照合：'+('、'.join(byid[x]['name_ja'] for x in b['reference_only_species_ids']) or 'このバッチ内の採用済み種なし')+'。','',
             '| 系列 | 連続して制作・確認する対象 | 他系列との差別化 | 構造・制作上の注意 |','|---|---|---|---|']
        for fid in b['family_ids']:
            f=next(x for x in cat['families'] if x['id']==fid)
            ids=[x for x in f['species_ids'] if x in b['species_ids']]
            s=byid[ids[0]]
            lines.append('| '+f['motif_ja']+' | '+' → '.join(byid[x]['name_ja'] for x in ids)+' | '+s['art']['differentiation_ja']+' | '+s['art']['anatomy_connections_ja']+' '+s['art']['production_difficulty_ja']+' |')
    lines += ['', '## 共通の確認手順','',
      '1. 既存原画・最新の採用範囲を確認し、同系列を並べて輪郭と成長差を照合する。',
      '2. 前・背・横で器官の数、付け根、主配色・差し色、識別点をそろえる。ホノル系列は腕2・脚2・独立翼2。ヨルミル系列は四肢4・独立翼0。',
      '3. 新しい三面設定は制作案として提示し、明確な採用回答を得てから次工程へ進める。「続行」を採用へ読み替えない。',
      '4. 後の96pxと32pxではJSONの残す特徴を使って判別を点検する。今回は縮小画像・ドット画像を作らない。',
      '5. 採用後の戦闘出力は前面が左下向き、背面が右上向き。設定画自体の向きと混同しない。']
    md('docs/SPECIES_ART_BATCHES_v0.1.md','\n'.join(lines))

if __name__=='__main__':
    cat=build()
    write_tables(cat)
    write_batches(cat)
    print(json.dumps({'species':len(cat['species']),'families':len(cat['families'])},ensure_ascii=False))
