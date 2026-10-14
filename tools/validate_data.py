"""Validate public source receipts and prohibit invented or mixed benchmark records."""
from pathlib import Path
import json
import math
import re
from urllib.parse import urlsplit

DEFAULT_ROOT=Path(__file__).resolve().parent.parent
class ValidationError(ValueError):
    pass

def read_json(path):
    def unique(pairs):
        result={}
        for key,value in pairs:
            if key in result: raise ValidationError('Duplicate JSON key: '+key)
            result[key]=value
        return result
    def constant(value): raise ValidationError('Non-finite JSON constant: '+value)
    return json.loads(Path(path).read_text(encoding='utf-8-sig'),object_pairs_hook=unique,parse_constant=constant)

def url(value):
    if not isinstance(value,str): raise ValidationError('Source URL must be text.')
    parsed=urlsplit(value)
    if parsed.scheme not in {'https','http'} or not parsed.hostname or parsed.username or parsed.password or any(c.isspace() for c in value):
        raise ValidationError('Source URL must be public HTTP(S), without credentials.')

def validate(data):
    if data.get('schemaVersion')!=1 or data.get('format')!='codex-frontier-observatory-v1': raise ValidationError('Unsupported data format.')
    compiler=data['compiler']
    if compiler['harness']!='codex' or compiler['computer']!='surface-arm': raise ValidationError('This contribution identifies surface-arm/codex only.')
    if 'model' not in compiler or (compiler['model'] is not None and not isinstance(compiler['model'],str)): raise ValidationError('Compiler model must be recorded or explicit null.')
    models={model['slug']:model for model in data['models']}
    if len(models)!=len(data['models']): raise ValidationError('Duplicate model slug.')
    for model in models.values():
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',model['slug']): raise ValidationError('Invalid model slug.')
    seen=set(); metrics={}
    for row in data['records']:
        required={'id','model','benchmark','benchmarkVersion','benchmarkId','value','unit','higherIsBetter','publisher','sourceType','setting','sourceUrl','sourceDate','readOn','sourceRead','origin','note','costUsd','durationMinutes'}
        if not required.issubset(row): raise ValidationError('Observation is missing receipt fields.')
        if row['id'] in seen: raise ValidationError('Duplicate observation.')
        seen.add(row['id'])
        if row['model'] not in models: raise ValidationError('Unknown scored model.')
        url(row['sourceUrl'])
        if row['sourceType'] not in {'claim','rival-table','independent'}: raise ValidationError('Invalid evidence type.')
        if type(row['sourceRead']) is not bool or type(row['higherIsBetter']) is not bool: raise ValidationError('Read/direction flags must be explicit booleans.')
        if not isinstance(row['setting'],dict): raise ValidationError('Setup must be an object.')
        if row['origin'] in {'quoted','derived'} and not row['note'].strip(): raise ValidationError('Quoted or derived value needs an explanation.')
        for key in ('value','costUsd','durationMinutes'):
            number=row[key]
            if number is not None and (isinstance(number,bool) or not isinstance(number,(float,int)) or not math.isfinite(number)): raise ValidationError('Values must be finite numbers or null.')
            if key!='value' and number is not None and number<0: raise ValidationError('Costs and durations must be nonnegative.')
        if row['unit']=='percent' and row['value'] is not None and not 0<=row['value']<=100: raise ValidationError('Percent is outside 0–100.')
        metric=(row['unit'],row['higherIsBetter'])
        if row['benchmarkId'] in metrics and metrics[row['benchmarkId']]!=metric: raise ValidationError('Use a separate benchmark ID when unit/direction changes.')
        metrics[row['benchmarkId']]=metric
    return data

if __name__=='__main__':
    data=validate(read_json(DEFAULT_ROOT/'data.json'))
    print(f'Validated {len(data["records"])} source observations; compiler model: {data["compiler"]["model"] or "not captured"}.')
