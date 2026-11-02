"""156種の設計・参照・抽象入手経路を検査。プレイテストではない。"""
from pathlib import Path
from collections import Counter
import copy
import csv
import hashlib
import json
import re
import subprocess
import sys
import unicodedata

ROOT=Path(__file__).resolve().parents[1]
CAT='content/planning/species-catalog_v0.1.json'
SCHEMA='content/planning/species-catalog_v0.1.schema.json'
REPORT='reports/species-catalog-check_v0.1.json'
def load(n):return json.loads((ROOT/n).read_text(encoding='utf-8'))
def obj(props, optional=()):
    return {'type':'object','properties':props,'required':[k for k in props if k not in optional],'additionalProperties':False}
def arr(item,minimum=0):return {'type':'array','items':item,'minItems':minimum}
STR={'type':'string','minLength':1}
BOOL={'type':'boolean'}
INT={'type':'integer','minimum':0}
SID={'type':'string','pattern':'^[a-z][a-z0-9_]+$','minLength':1}
NULL={'type':'null'}
def nullable(s):return {'anyOf':[s,NULL]}

def make_schema(types,regions):
    typ={'type':'string','enum':types}
    region={'type':'string','enum':regions}
    condition=obj({'method':{'enum':['level','level_at_time','site_interaction']},'level':{'type':'integer','minimum':1},
       'site_id':SID,'time':{'enum':['night','day','evening']},'status':{'enum':['confirmed','production_proposal']},
       'text_ja':STR,'unlock_story_rank':INT},optional=('level','site_id','time'))
    nextcondition=copy.deepcopy(condition)
    nextcondition['properties']['id']=SID;nextcondition['required'].append('id')
    method=obj({'method':{'enum':['evolution','starter_choice','postgame_rescue','wild_capture','fixed_repeatable']},
      'source_species_id':SID,'condition':condition,'region_id':nullable(region),'story_rank':INT,
      'required_field_move_ids':arr(SID),'solo':{'const':True},'repeatable':BOOL,'external_requirement':{'const':False},
      'encounter_time':nullable({'enum':['all','day','night','evening']}),'text_ja':STR,'choice_family_id':SID},
      optional=('source_species_id','condition','choice_family_id'))
    anatomy=obj({k:INT for k in ['independent_arms','legs','independent_wings','tails','horns','antennae','fins','tentacles']})
    artstatus=obj({k:STR for k in ['concept_direction','model_sheet','runtime_art','new_anatomy_detail','note_ja']})
    stats=obj({k:{'enum':['控えめ','標準','高め']} for k in ['hp','attack','defense','special_attack','special_defense','speed']})
    move=obj({'id':SID,'name_ja':STR,'effect_ja':STR,'type_candidates':arr(typ,1),'power':NULL,'accuracy':NULL,
              'usage_count':NULL,'status':{'const':'production_proposal'},'note_ja':STR})
    battle=obj({'role_id':SID,'role_ja':STR,'ability_trends':stats,'ability_trends_scope':STR,'strengths_ja':STR,'weaknesses_ja':STR,
      'received_type_multipliers':obj({t:{'type':'number','enum':[0,0.25,0.5,1,2,4]} for t in types}),
      'weak_to_type_ids':arr(typ),'resists_type_ids':arr(typ),'immune_type_ids':arr(typ),
      'damage_basis':STR,'move_direction_ja':STR,'signature_move':move,'numeric_stats_status':{'const':'not_designed'}})
    learn=obj({'move_id':SID,'name_ja':STR,'method':{'const':'reusable_free_lesson'},'unlock_story_rank':INT,
        'teacher_region_id':region,'status':{'const':'production_proposal'},'text_ja':STR})
    exploration=obj({'role_ja':STR,'field_move_ids':arr(SID),'learn_methods':arr(learn),'battle_slots_used_per_move':{'const':1},
        'requires_currently_learned_move':{'const':True},'requires_in_party':{'const':True},'status':STR})
    habitat=obj({'primary_region_id':region,'environment_ja':STR,'ecology_ja':STR,'environment_status':{'const':'production_proposal'},
        'wild_locations':arr(obj({'region_id':region,'environment_ja':STR,'access':STR})),'note_ja':STR})
    acquisition=obj({'first_available_ja':STR,'earliest_story_rank':INT,'methods':arr(method,1),
        'rarity':{'enum':['common','uncommon','rare','gift','fixed_repeatable','evolution_only']},'rarity_ja':STR,
        'appearance_conditions_ja':STR,'phase':{'enum':['main_story','postgame','choice_dependent_main_and_postgame']},
        'repeatable_source_ja':STR,'acquisition_status':{'const':'production_proposal'},'no_external_requirements':{'const':True}})
    art=obj({'motifs_ja':STR,'full_body_silhouette_ja':STR,'palette_main':arr(STR,1),'palette_accents':arr(STR),
        'palette_status':STR,'face_expression_ja':STR,'anatomy_counts':anatomy,'anatomy_connections_ja':STR,
        'anatomy_scope_ja':STR,'view_invariants':obj({'front_ja':STR,'back_ja':STR,'side_ja':STR}),
        'evolution_changes_ja':STR,'family_retained_features_ja':STR,'sprite_96px_ja':STR,'icon_32px_ja':STR,
        'differentiation_ja':STR,'production_difficulty_ja':STR,'art_adoption':artstatus,
        'explicit_anatomy_constraint':{'type':'object'}},optional=('explicit_anatomy_constraint',))
    provenance=obj({'origin':{'enum':['existing_with_proposed_details','new_production_proposal']},'name_status':STR,
        'typing_status':STR,'original_concept_status':STR,'game_design_status':{'enum':['proposal_with_inherited_decisions','production_proposal']},
        'confirmed_inherited_fields':arr(STR),'source_paths':arr(STR,1),'source_asset_ids':arr(SID),
        'legacy_card_snapshot':nullable({'type':'object'}),'new_fields_status':{'const':'production_proposal'},
        'user_adopted_new_design':{'const':False},'change_proposals':arr({'type':'object'},1)})
    species=obj({'dex_number':{'type':'integer','minimum':1,'maximum':156},'id':SID,'name_ja':STR,'family_id':SID,
       'evolution_stage':{'type':'integer','minimum':1,'maximum':3},'family_stage_count':{'type':'integer','minimum':1,'maximum':3},
       'evolves_from':nullable(SID),'evolves_to':nullable(nextcondition),'evolution_condition_from':nullable(condition),
       'primary_type':typ,'secondary_type':nullable(typ),'allocation_bucket_id':SID,'allocation_region_id':nullable(region),
       'battle':battle,'exploration':exploration,'habitat':habitat,'acquisition':acquisition,'art':art,'provenance':provenance})
    schema={'$schema':'https://json-schema.org/draft/2020-12/schema',
      '$id':'urn:monorica:planning:species-catalog:0.1',
      'title':'MONORICA species catalog planning v0.1','type':'object',
      'required':['schema_version','purpose','status','design_draft_complete','approved_game_data_complete','art_complete',
        'created_date_jst','source_bundle','policy_ja','types','regions','allocation','role_definitions','field_moves','time_policy',
        'return_safety_policy','evolution_sites','families','species','unresolved_ja'],
      'properties':{'schema_version':{'const':'0.1'},'purpose':{'const':'planning_only_not_runtime'},
        'status':STR,'design_draft_complete':{'const':True},'approved_game_data_complete':{'const':False},'art_complete':{'const':False},
        'created_date_jst':STR,'source_bundle':STR,'policy_ja':arr(STR,1),'types':arr({'type':'object'},12),
        'regions':arr({'type':'object'},10),'allocation':{'type':'object'},'role_definitions':arr({'type':'object'},1),
        'field_moves':arr({'type':'object'},4),'time_policy':{'type':'object'},'return_safety_policy':{'type':'object'},
        'evolution_sites':arr(obj({'id':SID,'name_ja':STR,'region_id':region,'unlock_story_rank':INT,'access_required_gate_ids':arr(SID),
                'repeatable':{'const':True},'consumable_required':{'const':False},'status':{'const':'production_proposal'},'access_ja':STR})),
        'families':arr(obj({'id':SID,'allocation_bucket_id':SID,'species_ids':arr(SID,1),'stage_count':{'type':'integer','minimum':1,'maximum':3},
                         'motif_ja':STR,'status':STR}),1),
        'species':{'type':'array','minItems':156,'maxItems':156,'items':{'$ref':'#/$defs/species'}},'unresolved_ja':arr(STR)},
      'additionalProperties':False,'$defs':{'species':species}}
    return schema

def schema_errors(value,schema,root=None,path='$'):
    """この同梱スキーマが使うキーワードを全て評価する。外部の完全なJSON Schemaエンジンではない。"""
    if root is None:root=schema
    if '$ref' in schema:
        target=root
        for part in schema['$ref'].split('/')[1:]:target=target[part]
        return schema_errors(value,target,root,path)
    if 'anyOf' in schema:
        if any(not schema_errors(value,x,root,path) for x in schema['anyOf']):return []
        return [path+': anyOf failed']
    result=[]
    if 'const' in schema and value!=schema['const']:result.append(path+': const')
    if 'enum' in schema and value not in schema['enum']:result.append(path+': enum')
    typ=schema.get('type')
    ok={'object':isinstance(value,dict),'array':isinstance(value,list),'string':isinstance(value,str),
        'integer':type(value)==int,'number':type(value) in (int,float),'boolean':type(value)==bool,'null':value is None}
    if typ and not ok[typ]:return result+[path+': type '+typ]
    if isinstance(value,dict):
        for key in schema.get('required',[]):
            if key not in value:result.append(path+': missing '+key)
        for key,val in value.items():
            if key in schema.get('properties',{}):result+=schema_errors(val,schema['properties'][key],root,path+'.'+key)
            elif schema.get('additionalProperties') is False:result.append(path+': unexpected '+key)
    if isinstance(value,list):
        if len(value)<schema.get('minItems',0):result.append(path+': minItems')
        if len(value)>schema.get('maxItems',float('inf')):result.append(path+': maxItems')
        if 'items' in schema:
            for i,x in enumerate(value):result+=schema_errors(x,schema['items'],root,path+f'[{i}]')
    if isinstance(value,str):
        if len(value)<schema.get('minLength',0):result.append(path+': minLength')
        if 'pattern' in schema and not re.search(schema['pattern'],value):result.append(path+': pattern')
    if type(value) in (int,float):
        if value<schema.get('minimum',float('-inf')):result.append(path+': minimum')
        if value>schema.get('maximum',float('inf')):result.append(path+': maximum')
    return result

def graph_cycles(edges):
    visiting=set();done=set();cycles=[]
    def visit(n):
        if n in visiting:cycles.append(n);return
        if n in done:return
        visiting.add(n)
        for t in edges.get(n,[]):visit(t)
        visiting.remove(n);done.add(n)
    for n in edges:visit(n)
    return cycles

def simulate(cat,choice,max_rank):
    """イベント順序・親・地域・講習を満たす取得。レベル稼ぎ可能性は抽象仮定で実時間は扱わない。"""
    got=set();learned={};visited=set();gates=set();history=[]
    fields={x['id']:x for x in cat['field_moves']}
    sites={x['id']:x for x in cat['evolution_sites']}
    main=[x['id'] for x in cat['regions'] if x['phase']=='main_story']
    posts=[x['id'] for x in cat['regions'] if x['phase']=='postgame']
    region_ranks={rid:(10 if i==0 else (i+1)*10) for i,rid in enumerate(main)}
    for rid in posts:region_ranks[rid]=100
    for rank in range(10,max_rank+1):
        for rid,rr in region_ranks.items():
            if rr>rank:continue
            if rid==main[0]:visited.add(rid)
            elif rid==main[1] and 'field_vine' in gates:visited.add(rid)
            elif rid==main[2] and 'field_wave' in gates:visited.add(rid)
            elif rid==main[3] and 'field_ember' in gates:visited.add(rid)
            elif rid in main[4:] and main[main.index(rid)-1] in visited:visited.add(rid)
            elif rid in posts and rank>=100 and main[-1] in visited and len(gates)==4:visited.add(rid)
        changed=True
        while changed:
            changed=False
            for s in cat['species']:
                if s['id'] in got:continue
                for m in s['acquisition']['methods']:
                    if m['story_rank']>rank or not m['solo'] or m['external_requirement']:continue
                    if not set(m['required_field_move_ids']).issubset(gates):continue
                    method=m['method']
                    if method=='evolution':
                        cond=m['condition']
                        allowed=m['source_species_id'] in got
                        if cond['method']=='site_interaction':
                            site=sites.get(cond['site_id'])
                            allowed=allowed and site is not None and site['region_id'] in visited and site['unlock_story_rank']<=rank and set(site['access_required_gate_ids']).issubset(gates)
                        if cond['method']=='level_at_time':allowed=allowed and cat['time_policy']['clock']=='game_internal'
                    elif method=='starter_choice':allowed=m['choice_family_id']==choice and m['region_id'] in visited
                    elif method=='postgame_rescue':allowed=rank>=100 and m['region_id'] in visited
                    else:allowed=m['region_id'] in visited
                    if s['id']=='wild_dusk_glider_01' and 'field_vine' not in gates:allowed=False
                    if allowed:
                        got.add(s['id']);changed=True;history.append({'id':s['id'],'rank':rank,'method':method});break
            for s in cat['species']:
                if s['id'] not in got:continue
                for m in s['exploration']['learn_methods']:
                    if m['unlock_story_rank']<=rank and m['teacher_region_id'] in visited:
                        learned.setdefault(m['move_id'],set()).add(s['id'])
        for mid,m in fields.items():
            if m['gate_rank']==rank:
                # 必須前提：火の講習は岩の通路の後。通常種だけで解く。
                normal={x for x in learned.get(mid,set()) if not x.startswith('starter_')}
                if not normal or (mid=='field_ember' and 'field_break' not in gates):
                    return dict(success=False,rank=rank,blocked_gate=mid,obtained_count=len(got))
                gates.add(mid)
    return dict(success=True,obtained_count=len(got),obtained_ids=sorted(got),gates=sorted(gates),
      normal_gate_providers={mid:sorted(x for x in learned.get(mid,set()) if not x.startswith('starter_')) for mid in fields},
      visited_regions=sorted(visited),history=history)

def inspect(cat,known,world,chart):
    checks=[]
    def check(name,passed,details=None):checks.append({'id':name,'pass':bool(passed),'details':details})
    sp=cat['species'];ids=[s['id'] for s in sp];names=[unicodedata.normalize('NFC',s['name_ja']) for s in sp]
    byid={s['id']:s for s in sp};types=set(chart['type_order']);regions={r['id'] for r in world['regions']}
    check('species_count',len(sp)==156,len(sp))
    check('dex_1_to_156',sorted(s['dex_number'] for s in sp)==list(range(1,157)))
    check('unique_species_ids',len(set(ids))==len(ids))
    check('unique_names',len(set(names))==len(names))
    check('existing_15_exactly_once',all(ids.count(x['id'])==1 for x in known))
    check('existing_identity_and_snapshot',all(x['id'] in byid and byid[x['id']]['name_ja']==x['name_ja'] and
       byid[x['id']]['family_id']==x['family_id'] and byid[x['id']]['evolution_stage']==x['stage'] and
       byid[x['id']]['primary_type']==x['primary_type_candidate'] and byid[x['id']]['provenance']['legacy_card_snapshot']==x for x in known))
    edges={s['id']:([s['evolves_to']['id']] if s['evolves_to'] else []) for s in sp}
    valid_evo=True
    for s in sp:
        nxt=s['evolves_to'];par=s['evolves_from']
        if nxt:
            target=byid.get(nxt['id'])
            valid_evo=valid_evo and target is not None
            if target:
                valid_evo=valid_evo and target['family_id']==s['family_id'] and target['evolution_stage']==s['evolution_stage']+1 and target['evolves_from']==s['id']
                valid_evo=valid_evo and target['evolution_condition_from']=={k:v for k,v in nxt.items() if k!='id'}
        if par:valid_evo=valid_evo and par in byid and (byid[par]['evolves_to'] or {}).get('id')==s['id']
    check('evolution_references_and_reverse_links',valid_evo)
    check('evolution_acyclic',not graph_cycles(edges))
    starter=[s for s in sp if s['id'].startswith('starter_')]
    check('starter_conditions_16_36',len(starter)==9 and all((s['evolves_to'] is None if s['evolution_stage']==3 else
       s['evolves_to']['method']=='level' and s['evolves_to']['level']==(16 if s['evolution_stage']==1 else 36) and s['evolves_to']['status']=='confirmed') for s in starter))
    check('type_refs_and_max_two',all(s['primary_type'] in types and (s['secondary_type'] is None or s['secondary_type'] in types and s['secondary_type']!=s['primary_type']) for s in sp))
    check('region_refs',all((s['allocation_region_id'] is None or s['allocation_region_id'] in regions) and s['habitat']['primary_region_id'] in regions and
      all(m['region_id'] is None or m['region_id'] in regions for m in s['acquisition']['methods']) and
      all(x['region_id'] in regions for x in s['habitat']['wild_locations']) and
      all(x['teacher_region_id'] in regions for x in s['exploration']['learn_methods']) for s in sp))
    count=Counter(s['allocation_bucket_id'] for s in sp)
    check('original_region_allocation_unchanged',count['starter_pool']==9 and all(count[r['id']]==r['new_species_slots'] for r in world['regions']),dict(count))
    check('allocation_total_156',sum(count.values())==156)
    check('source_types_and_regions_retained',cat['types']==chart['types'] and cat['regions']==world['regions'])
    check('all12_normal_base_types_by_hinowa',len({s['primary_type'] for s in sp if s['evolution_stage']==1 and
        s['allocation_region_id'] in ['region_kazami','region_minase','region_hinowa']})==12)
    check('main8_post2_reps8',sum(r['phase']=='main_story' for r in cat['regions'])==8 and sum(r['phase']=='postgame' for r in cat['regions'])==2 and
      len({r['representative']['id'] for r in cat['regions'] if r['representative']})==8)
    check('no_new_adoption_claim',all(not s['provenance']['user_adopted_new_design'] and s['provenance']['new_fields_status']=='production_proposal' and
      (s['id'] in {x['id'] for x in known} or s['provenance']['game_design_status']==s['provenance']['name_status']==s['provenance']['typing_status']==s['art']['art_adoption']['concept_direction']=='production_proposal') for s in sp))
    check('no_fabricated_wild_evolution_locations',all(not s['habitat']['wild_locations'] and s['acquisition']['rarity']=='evolution_only' and
      all(m['method']=='evolution' for m in s['acquisition']['methods']) for s in sp if s['evolves_from']))
    check('solo_routes_no_external',all(s['acquisition']['no_external_requirements'] and any(m['solo'] and not m['external_requirement'] for m in s['acquisition']['methods']) for s in sp))
    check('evolution_conditions_supported',all(s['evolves_to'] is None or s['evolves_to']['method'] in ['level','level_at_time','site_interaction'] for s in sp))
    sites={x['id']:x for x in cat['evolution_sites']}
    check('evolution_site_refs_and_repeatable_access',len(sites)==len(cat['evolution_sites']) and all(x['region_id'] in regions and x['repeatable'] and
        not x['consumable_required'] for x in sites.values()) and all((s['evolves_to']['site_id'] in sites and
        s['evolves_to']['unlock_story_rank']==sites[s['evolves_to']['site_id']]['unlock_story_rank']) for s in sp if s['evolves_to'] and s['evolves_to']['method']=='site_interaction'))
    check('no_unverified_numeric_stats',all(s['battle']['numeric_stats_status']=='not_designed' and all(s['battle']['signature_move'][k] is None for k in ['power','accuracy','usage_count']) for s in sp))
    matches=True
    for s in sp:
        expected={}
        for atk in chart['type_order']:
            v=chart['damage_multipliers'][atk][s['primary_type']]
            if s['secondary_type']:v*=chart['damage_multipliers'][atk][s['secondary_type']]
            expected[atk]=v
        matches=matches and expected==s['battle']['received_type_multipliers']
        matches=matches and s['battle']['weak_to_type_ids']==[t for t,v in expected.items() if v>1]
        matches=matches and s['battle']['resists_type_ids']==[t for t,v in expected.items() if 0<v<1]
        matches=matches and s['battle']['immune_type_ids']==[t for t,v in expected.items() if v==0]
    check('all_1872_type_products',matches,156*12)
    check('honoru_family_6_limbs',all(s['art']['anatomy_counts']['independent_arms']==2 and s['art']['anatomy_counts']['legs']==2 and
        s['art']['anatomy_counts']['independent_wings']==2 for s in sp if s['family_id']=='starter_ember_wyvern'))
    check('yorumiru_family_4_limbs',all(s['art']['anatomy_counts']['independent_arms']==0 and s['art']['anatomy_counts']['legs']==4 and
        s['art']['anatomy_counts']['independent_wings']==0 for s in sp if s['family_id']=='wild_dusk_glider'))
    pending=['wild_stream_otter_01','wild_coil_dormouse_01','wild_dusk_glider_01']
    check('pending_art_not_adopted',all(byid[s]['art']['art_adoption']['model_sheet']=='visual_review_pending' and
       byid[s]['art']['art_adoption']['runtime_art']=='not_created' for s in pending if s in byid) and all(x in byid for x in pending))
    adopted={s['id'] for s in sp if s['art']['art_adoption']['runtime_art']=='static_sprites_visual_adopted_technical_checked'}
    check('adopted_6_species_sprites_unchanged',adopted=={'starter_flower_hare_01','starter_ember_wyvern_01','starter_tide_bear_01','wild_seed_squirrel_01','wild_vine_mole_01','wild_breeze_bird_01'})
    fs={f['id']:f for f in cat['families']}
    famids=[f['id'] for f in cat['families']]
    check('family_membership_stages',len(set(famids))==len(famids) and all(s['family_id'] in fs and s['id'] in fs[s['family_id']]['species_ids'] and
       fs[s['family_id']]['stage_count']==s['family_stage_count'] for s in sp) and
       all(f['stage_count']==len(f['species_ids']) and all(x in byid for x in f['species_ids']) for f in cat['families']))
    moves={x['id']:x for x in cat['field_moves']}
    check('field_move_references',len(moves)==4 and all(set(s['exploration']['field_move_ids'])=={m['move_id'] for m in s['exploration']['learn_methods']} and
       set(s['exploration']['field_move_ids']).issubset(moves) for s in sp))
    check('field_four_slots_and_party',all(s['exploration']['battle_slots_used_per_move']==1 and s['exploration']['requires_currently_learned_move'] and
        s['exploration']['requires_in_party'] and len(s['exploration']['field_move_ids'])<=4 for s in sp))
    check('normal_base_providers_before_gates',all(m['primary_provider'] in byid and not m['primary_provider'].startswith('starter_') and
       byid[m['primary_provider']]['evolution_stage']==1 and byid[m['primary_provider']]['acquisition']['earliest_story_rank']<m['learn_rank']<m['gate_rank'] and
       m['id'] in byid[m['primary_provider']]['exploration']['field_move_ids'] for m in moves.values()))
    check('field_relearn_preserved_on_evolution',all(set(s['exploration']['field_move_ids']).issubset(byid[s['evolves_to']['id']]['exploration']['field_move_ids'])
         for s in sp if s['evolves_to'] and s['evolves_to']['id'] in byid))
    # 条件参照の有向依存グラフ。講習は必要地点前、地点は地域の解禁後。
    dependency={}
    for s in sp:
        deps=[]
        for m in s['acquisition']['methods']:
            if m['method']=='evolution':deps.append('species:'+m['source_species_id'])
            elif m.get('region_id'):deps.append('region:'+m['region_id'])
        dependency['species:'+s['id']]=deps
    main_regions=[r['id'] for r in world['regions'] if r['phase']=='main_story']
    for i,rid in enumerate(main_regions):
        dependency['region:'+rid]=[] if i==0 else ['region:'+main_regions[i-1]]
    for rid in ['post_shizuna','post_meguri']:dependency['region:'+rid]=['region:region_hoshimi']
    for mid,m in moves.items():
        dependency['learn:'+mid]=['species:'+m['primary_provider'],'region:'+m['region_id']]
        dependency['gate:'+mid]=['learn:'+mid]
    check('acquisition_and_field_dependency_acyclic',not graph_cycles(dependency),
          '複数入手方法は代替経路であり、全て同時必須ではない。御三家の分岐は別の3ケース検査。')
    sims={}
    if valid_evo and len(moves)==4 and all(m['primary_provider'] in byid for m in moves.values()):
        for family in ['starter_flower_hare','starter_ember_wyvern','starter_tide_bear']:
            main=simulate(cat,family,89);post=simulate(cat,family,102)
            sims[family]={'main':main,'postgame':post}
        check('all_three_choices_main132_post156',all(x['main']['success'] and x['main']['obtained_count']==132 and
           x['postgame']['success'] and x['postgame']['obtained_count']==156 for x in sims.values()),
           {k:{'main':v['main'].get('obtained_count'),'postgame':v['postgame'].get('obtained_count')} for k,v in sims.items()})
        check('unchosen_starters_postgame_only',all(all(not h['id'].startswith('starter_') or h['id'].startswith(k+'_') for h in v['main'].get('history',[])) for k,v in sims.items()))
    else:check('all_three_choices_main132_post156',False,'先行の参照エラーでシミュレーションを保留。')
    return checks,sims

def main():
    cat=load(CAT);world=load('content/planning/world-outline.json');chart=load('content/type-chart.json');known=load('content/planning/known-species.json')['species']
    schema=make_schema(chart['type_order'],[r['id'] for r in world['regions']])
    (ROOT/SCHEMA).write_text(json.dumps(schema,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    serr=schema_errors(cat,schema)
    checks,sims=inspect(cat,known,world,chart)
    checks.insert(0,{'id':'common_json_schema','pass':not serr,'details':serr})
    def extra(name,ok,detail=None):checks.append({'id':name,'pass':bool(ok),'details':detail})
    byid={s['id']:s for s in cat['species']}
    assets=load('manifests/assets.json');aid={a['id']:a for a in assets['entries']}
    extra('source_paths_and_asset_refs',all((ROOT/p).is_file() for s in cat['species'] for p in s['provenance']['source_paths']) and
          all(x in aid and aid[x]['state']!='rejected_anatomy_superseded' for s in cat['species'] for x in s['provenance']['source_asset_ids']))
    extra('yorumiru_reference_v02_only','source_yorumiru_model_sheet_v02' in byid['wild_dusk_glider_01']['provenance']['source_asset_ids'] and
          'source_yorumiru_model_sheet_v01' not in byid['wild_dusk_glider_01']['provenance']['source_asset_ids'])
    baseline_record=load('reports/species-catalog-source-baseline_v0.1.json')
    baseline=baseline_record['original_file_hashes']
    changed=[];missing=[]
    for n,h in baseline.items():
        p=ROOT/n
        if not p.is_file():missing.append(n)
        elif hashlib.sha256(p.read_bytes()).hexdigest()!=h:changed.append(n)
    allowed=['LATEST_HANDOFF.md','README.md','docs/DECISIONS.md']
    extra('original_bundle_preserved',not missing and set(changed).issubset(allowed),{'original_files':len(baseline),'missing':missing,'changed':changed,'allowed_document_updates':allowed})
    protected=[n for n in baseline if n.startswith(('assets/','brief/','manifests/','content/'))]
    extra('original_art_and_planning_hashes_unchanged',all(n not in changed and n not in missing for n in protected),{'protected_file_count':len(protected)})
    with (ROOT/'content/planning/species-catalog_v0.1.csv').open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
    extra('csv_json_alignment',len(rows)==156 and all(int(r['図鑑番号'])==s['dex_number'] and r['種ID']==s['id'] and r['名前']==s['name_ja'] for r,s in zip(rows,cat['species'])))
    mdtext=(ROOT/'docs/SPECIES_CATALOG_v0.1.md').read_text(encoding='utf-8')
    extra('markdown_all156_rows',len(re.findall(r'^\| \d{3} \|',mdtext,re.M))==156 and all(s['name_ja'] in mdtext for s in cat['species']))
    batches=load('content/planning/species-art-batches_v0.1.json')
    batchids=[x for b in batches['batches'] for x in b['species_ids']]
    refs=batches['reference_only_adopted_species']
    extra('art_batches_10_to15_150_plus6',all(10<=len(b['species_ids'])<=15 for b in batches['batches']) and
          len(batchids)==150 and len(set(batchids))==150 and len(refs)==6 and set(batchids).isdisjoint(refs) and set(batchids+refs)==set(byid),
          [len(b['species_ids']) for b in batches['batches']])
    extra('art_batches_no_family_split',all(len({b['id'] for b in batches['batches'] if any(x in b['species_ids'] for x in f['species_ids'])})==1 for f in cat['families']))
    # 最小限の故障注入で検査が代表的な誤りを検出することも点検。
    negatives=[]
    def negative(name,mutator,expected):
        bad=copy.deepcopy(cat);mutator(bad)
        try:
            result,_=inspect(bad,known,world,chart)
            found=any(c['id']==expected and not c['pass'] for c in result)
        except (KeyError,TypeError,IndexError):found=False
        negatives.append({'id':name,'detected':found,'expected_check':expected})
    negative('duplicate_id',lambda c:c['species'][1].update(id=c['species'][0]['id']),'unique_species_ids')
    negative('duplicate_name',lambda c:c['species'][1].update(name_ja=c['species'][0]['name_ja']),'unique_names')
    negative('missing_number',lambda c:c['species'][1].update(dex_number=1),'dex_1_to_156')
    negative('starter_level_17',lambda c:c['species'][0]['evolves_to'].update(level=17),'starter_conditions_16_36')
    negative('new_adoption_false_claim',lambda c:c['species'][-1]['provenance'].update(user_adopted_new_design=True),'no_new_adoption_claim')
    negative('removed_field_provider',lambda c:c['species'][11]['exploration'].update(field_move_ids=[],learn_methods=[]),'normal_base_providers_before_gates')
    negative('wing_arm_regression',lambda c:c['species'][3]['art']['anatomy_counts'].update(independent_arms=0),'honoru_family_6_limbs')
    negative('six_leg_glider_regression',lambda c:c['species'][19]['art']['anatomy_counts'].update(legs=6),'yorumiru_family_4_limbs')
    extra('negative_control_detection',all(x['detected'] for x in negatives),negatives)
    validators=[]
    for script in ['validate_assets.py','validate_preproduction.py']:
        process=subprocess.run([sys.executable,str(ROOT/'tools'/script)],cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
        try:out=json.loads(process.stdout)
        except json.JSONDecodeError:out={'stdout':process.stdout}
        validators.append({'script':'tools/'+script,'exit_code':process.returncode,'output':out,'stderr':process.stderr})
    extra('legacy_validators_pass',all(v['exit_code']==0 for v in validators))
    readable=['AGENTS.md','CLAUDE.md','LATEST_HANDOFF.md','HANDOFF_MONORICA_2026-11-02_v0.12.md','docs/DECISIONS.md',
      'docs/WORLD_OUTLINE_v0.1.md','docs/STORY_CONFLICT_B_v0.1.md','content/planning/world-outline.json',
      'content/planning/known-species.json','content/type-chart.json','docs/STARTER_MODEL_SHEETS_v0.1.md',
      'docs/EARLY_WILD_MODEL_SHEETS_v0.1.md','docs/LATER_WILD_MODEL_SHEETS_v0.1.md',
      'brief/07_starter_evolution_plan_v0.1.md','brief/10_starter_playstyle_proposal_v0.2.md',
      'brief/11_field_moves_and_opening_v0.2.md','brief/12_first_region_proposal_v0.3.md','brief/14_early_wild_creatures_v0.2.md',
      'brief/06_starter_signature_design_brief_v0.2.md','tools/validate_assets.py','tools/validate_preproduction.py']
    visual=['brief/starter_concepts_v0.4.png','brief/starter_middle_concepts_v0.1.png','brief/wild_monsters_concepts_v0.1.png']
    for sid in ['starter_flower_hare_01','starter_ember_wyvern_01','starter_tide_bear_01','wild_seed_squirrel_01','wild_vine_mole_01','wild_breeze_bird_01','wild_stream_otter_01','wild_coil_dormouse_01','wild_dusk_glider_01']:
        model=next(x for x in known if x['id']==sid)['model_sheet_asset_id'];visual.append(aid[model]['path'])
    source_audit={'bundle_name':baseline_record['source_bundle'],'bundle_sha256':baseline_record['source_bundle_sha256'],
       'hash_source_ja':'元ZIP展開直後の計測を同梱baselineへ保存。検査の再実行に元ZIPを要求しない。',
       'documents_read':readable,'images_visually_inspected':visual,'unavailable_required_sources':[],
       'note_ja':'最初は取得に失敗したが、ユーザーがWindows作業フォルダーへ配置したZIPを展開して必要資料を読んだ。初回失敗を資料読了へ読み替えていない。'}
    summary={
       'species_count':len(cat['species']),'family_count':len(cat['families']),
       'stage_family_counts':dict(Counter(str(f['stage_count']) for f in cat['families'])),
       'primary_type_counts':dict(Counter(s['primary_type'] for s in cat['species'])),
       'secondary_type_counts':dict(Counter(s['secondary_type'] for s in cat['species'] if s['secondary_type'])),
       'allocation':dict(Counter(s['allocation_bucket_id'] for s in cat['species'])),
       'role_counts':dict(Counter(s['battle']['role_id'] for s in cat['species'])),
       'existing_species':15,'newly_added_species':141,'new_names_from_previous_world_proposals':6,'wholly_new_species_proposals':135,
       'runtime_png_count':assets['runtime_image_count'],'runtime_ready_png_count':assets['runtime_ready_image_count']}
    report={'schema_version':'0.1','created_date_jst':'2026-11-02','status':'pass' if all(x['pass'] for x in checks) else 'fail',
      'scope_ja':'設計表の件数・参照・抽象の入手依存・既存素材不変の検査。実ゲーム・面白さ・バランスの検証ではない。',
      'schema_engine_ja':'同梱スキーマが使用する型・必須・anyOf・参照・列挙・定数・範囲・配列長・文字列長・パターンをローカル実装で検査。外部JSON Schema実装は未導入。',
      'summary':summary,'source_audit':source_audit,'checks':checks,'passed_check_count':sum(x['pass'] for x in checks),
      'failed_check_count':sum(not x['pass'] for x in checks),'starter_choice_simulations':sims,'existing_validators':validators,
      'simulation_assumptions_ja':['捕獲は通常の再試行で可能、道具は通常の補充が可能とする設計前提。成功確率・経済は未検証。',
        '必要レベルまでは育成可能とする。経験値曲線・所要時間は未設定。','昼夜待機・無償再講習・固定戦再挑戦は制作案で、ゲーム内挙動は未実装。',
        '地域接続はworld-outlineの順序を用いる。タイル・帰路・全滅・技忘却の状態空間は実ゲームで未検証。'],
      'unresolved':cat['unresolved_ja'],'game_balance_verified':False,'fun_verified':False,'playthrough_verified':False,
      'image_generation_performed':False,'game_implementation_performed':False,'git_commit_push_or_publish_performed':False}
    (ROOT/REPORT).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':report['status'],'checks':len(checks),'passed':report['passed_check_count'],
        'failed':[x for x in checks if not x['pass']]},ensure_ascii=False,indent=2))
    return 0 if report['status']=='pass' else 1

if __name__=='__main__':raise SystemExit(main())
