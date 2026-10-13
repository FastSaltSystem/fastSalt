"""Shared, unit-explicit main coolant model and projections (Python 3.11+).

No geometry, drawing coordinates or solver equations belong in this document.
The adapters derive units/aliases and simple pump arithmetic, not new sizing.
"""
from copy import deepcopy
import hashlib
import json
import math
from pathlib import Path
import tomllib

DEFAULT_MODEL = Path(__file__).resolve().parents[1] / 'coolant-system.toml'
CASE_UNITS = {'mass_flow':'kg/s', 'density':'kg/m3', 'generator_pressure_drop':'Pa',
              'loop_allowance':'1', 'pump_efficiency':'1', 'motor_efficiency':'1',
              'motor_rating':'kW', 'hot_temperature':'K', 'cold_temperature':'K',
              'generator_duty':'MW', 'secondary_pressure':'MPa_abs'}
STATUSES = {'provisional_assumption','inherited_basis','design_target',
            'screening_assumption','conditional_dimension'}


def validate(model):
    def require(ok, message):
        if not ok:
            raise ValueError(message)
    require(model.get('schema_version') == 1, 'Unsupported coolant schema')
    require(model['system']['active_case'] == 'normal', 'Only the normal case has view adapters')
    def quantity(item, unit):
        value = item['value']
        require(type(value) in (float,int) and math.isfinite(value) and value > 0,
                'Quantity must be finite and positive')
        require(item['unit'] == unit, f'Expected unit {unit}, got {item["unit"]}')
        require(item['source'] in model['sources'], 'Unknown quantity source')
        require(item['status'] in STATUSES and bool(item['locator']), 'Missing quantity status/locator')
    normal = model['cases']['normal']
    require(set(normal) == set(CASE_UNITS), 'Unsupported or missing normal-case quantities')
    for key,unit in CASE_UNITS.items():
        quantity(normal[key],unit)
    for key in ('pump_efficiency','motor_efficiency'):
        require(normal[key]['value'] <= 1, 'Efficiency exceeds one')
    quantity(model['cases']['wall_screening']['pressure'], 'MPa_g')
    for spec in model['specifications'].values():
        require(set(spec) == {'bore','wall','insulation'}, 'Unknown or missing pipe quantity')
        for q in spec.values():
            quantity(q,'m')
    components = model['components']; ports=set()
    for tag,c in components.items():
        require(c['parent'] == model['system']['id'], f'{tag}: unknown system parent')
        require(c['type'] in ('reactor','heat_exchanger','pump'), f'{tag}: unsupported component type')
        require(len(c['ports']) == len(set(c['ports'])), f'{tag}: duplicate port')
        ports.update(tag+'.'+port for port in c['ports'])
    for tag,c in model['connections'].items():
        require(c['specification'] in model['specifications'], f'{tag}: unknown specification')
        require(len(c['via']) == len(set(c['via'])), f'{tag}: duplicate via equipment')
        for pump in c['via']:
            require(components.get(pump,{}).get('type') == 'pump', f'{tag}: via is not a pump')
        for start,end in segments(c):
            require(start in ports and end in ports and start != end, f'{tag}: invalid connection endpoint')
    return model


def segments(connection):
    start=connection['from']; result=[]
    for pump in connection['via']:
        result.append((start,pump+'.suction'));start=pump+'.discharge'
    return result+[(start,connection['to'])]


def read(path=DEFAULT_MODEL):
    path=Path(path).resolve()
    model=validate(tomllib.loads(path.read_text()))
    hub=path.parents[2]
    # A worksheet edit cannot silently become an adopted graphics/design input.
    for name,source in model['sources'].items():
        file=(hub/source['path']).resolve()
        if not file.is_relative_to(hub):
            raise ValueError(f'{name}: source must be inside project hub')
        if hashlib.sha256(file.read_bytes()).hexdigest() != source['sha256']:
            raise ValueError(f'{name}: worksheet changed; review adopted values before updating source hash')
    model['_provenance']={'model_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                          'adapter_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                          'sources':deepcopy(model['sources'])}
    return model


def value(model,key):
    return model['cases']['normal'][key]['value']


def pipe_specs(model):
    result={}
    for name,spec in model['specifications'].items():
        p={key:q['value'] for key,q in spec.items()}
        p['bare_od']=p['bore']+2*p['wall'];p['jacket_od']=p['bare_od']+2*p['insulation']
        result[name]=p
    return result


def pump_inputs(model):
    names={'mass_flow_kg_s':'mass_flow','density_kg_m3':'density',
           'sg_pressure_drop_pa':'generator_pressure_drop','allowance_factor':'loop_allowance',
           'pump_efficiency':'pump_efficiency','motor_efficiency':'motor_efficiency',
           'motor_rating_kw':'motor_rating'}
    return {name:value(model,key) for name,key in names.items()}


def pid_projection(model):
    """Return the shared portion of the existing P&ID schema, with explicit units."""
    validate(model)
    equipment=deepcopy(model['components'])
    for c in equipment.values():
        c.pop('parent')
        if c['type']=='heat_exchanger':c['duty_MWth']=value(model,'generator_duty')
    specs=pipe_specs(model);lines={}
    for tag,c in model['connections'].items():
        service=c['specification'];spec=specs[service]
        lines[tag]={k:deepcopy(c[k]) for k in ('from','to','via','status')}
        lines[tag].update(bore_mm=1000*spec['bore'],wall_mm=1000*spec['wall'],
                          od_mm=1000*spec['bare_od'],radial_insulation_mm=1000*spec['insulation'],
                          temperature_C=round(value(model,service+'_temperature')-273.15,8),heated=None)
    flow=value(model,'mass_flow')/value(model,'density')
    rise=value(model,'generator_pressure_drop')*value(model,'loop_allowance')
    # Preserve the worksheet's seven significant figures in existing drawing labels/registers.
    rounded=lambda x:float(format(x,'.7g'))
    basis=dict(flow_m3_s=rounded(flow),pump_rise_kPa=rounded(rise/1000),
               shaft_MW=rounded(flow*rise/value(model,'pump_efficiency')/1e6),
               motor_MW=value(model,'motor_rating')/1000,
               screening_pressure_MPag=model['cases']['wall_screening']['pressure']['value'],
               secondary_pressure_MPaa=value(model,'secondary_pressure'))
    return dict(equipment=equipment,lines=lines,basis=basis)


def merge_pid(view, model):
    result=deepcopy(view);shared=pid_projection(model)
    if 'basis' in result:
        raise ValueError('P&ID must not override shared basis')
    result['basis']=shared['basis']
    for group in ('equipment','lines'):
        imported=set()
        for tag,item in result[group].items():
            if item.get('shared') is True:
                allowed={'shared','sheet'} if group=='lines' else {'shared'}
                if set(item)-allowed:raise ValueError(f'{tag}: local override of shared engineering data')
                if tag not in shared[group]:raise ValueError(f'{tag}: missing from shared model')
                result[group][tag]={**shared[group][tag],**{k:v for k,v in item.items() if k!='shared'}}
                imported.add(tag)
            elif tag in shared[group]:
                raise ValueError(f'{tag}: shared identity duplicated locally')
        if imported != set(shared[group]):raise ValueError(f'P&ID missing shared {group}')
    result['shared_provenance']=deepcopy(model.get('_provenance',{}))
    return result


def graphics_legs(model):
    """Read leg topology from shared connections; no hard-coded pipe endpoint graph."""
    validate(model);legs=[];used=set()
    for tag,hot in model['connections'].items():
        if hot['specification']!='hot':continue
        reactor,hot_port=hot['from'].rsplit('.',1);sg,inlet=hot['to'].rsplit('.',1)
        candidates=[(t,c) for t,c in model['connections'].items()
                    if c['from']==sg+'.salt_outlet' and c['specification']=='cold']
        if len(candidates)!=1:raise ValueError(f'{tag}: graphics needs one cold return per generator')
        cold_tag,cold=candidates[0]
        if inlet!='salt_inlet' or hot['via'] or len(cold['via'])!=1 or cold['to'].split('.')[0]!=reactor:
            raise ValueError(f'{tag}: topology unsupported by current graphics adapter')
        if model['components'][reactor]['type']!='reactor' or model['components'][sg]['type']!='heat_exchanger':
            raise ValueError(f'{tag}: wrong graphics equipment type')
        legs.append(dict(reactor=reactor,generator=sg,pump=cold['via'][0],hot_line=tag,cold_line=cold_tag,
                         hot_port=hot['from'],cold_port=cold['to']))
        used.update((tag,cold_tag))
    if len(legs)!=3 or used!=set(model['connections']):
        raise ValueError('Current graphics adapter requires exactly three complete legs')
    for key in ('generator','pump','hot_port','cold_port'):
        if len({leg[key] for leg in legs})!=len(legs):raise ValueError(f'Duplicate leg {key}')
    if len({leg['reactor'] for leg in legs})!=1:raise ValueError('Multiple reactor interfaces unsupported')
    return legs


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model',type=Path,default=DEFAULT_MODEL)
    parser.add_argument('--output',type=Path,help='Optional detached engineering JSON snapshot for inspection')
    args=parser.parse_args();model=read(args.model);graphics_legs(model)
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(model,indent=2)+'\n')
    print(f"Validated {len(model['components'])} components and {len(model['connections'])} connections; worksheet hashes current")
