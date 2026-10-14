"""Build the self-contained Codex page and its public data using the standard library."""
from pathlib import Path
import hashlib
import html
import json
import shutil
import sys
from validate_data import validate, read_json

ROOT = Path(__file__).resolve().parent.parent

def resolve_output(root, output=None):
    root = Path(root).resolve()
    output = Path('dist') if output is None else Path(output)
    destination = (output if output.is_absolute() else root/output).resolve()
    if root.is_relative_to(destination) or not destination.is_relative_to(root):
        raise ValueError('Output must be a separate generated directory inside this project.')
    relative = destination.relative_to(root)
    if relative.parts[0] in {'tools','web','snapshots','archive','charts','docs','tests'} or relative.parts[0].startswith('.'):
        raise ValueError('Output cannot replace source folders.')
    return destination

def script_json(value):
    return json.dumps(value,ensure_ascii=False,allow_nan=False).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026').replace('\u2028','\\u2028').replace('\u2029','\\u2029')

def build(root=ROOT):
    root=Path(root).resolve()
    data=read_json(root/'data.json'); validate(data)
    charts={path.stem:path.read_text(encoding='utf-8') for path in sorted((root/'charts').glob('*.html'), key=lambda path: path.name)}
    if len(charts)!=7:
        raise ValueError('The seven saved chart/receipt files are required.')
    hashes=read_json(root/'archive'/'initial-file-hashes.json')
    for name,digest in hashes.items():
        if hashlib.sha256((root/'charts'/name).read_bytes()).hexdigest()!=digest:
            raise ValueError('Initial chart archive changed: '+name)
    template=(root/'web'/'template.html').read_text(encoding='utf-8')
    for token,value in [('__STYLE__',(root/'web'/'style.css').read_text(encoding='utf-8')),('__DATA__',script_json(data)),('__CHARTS__',script_json(charts)),('__APP__',(root/'web'/'app.js').read_text(encoding='utf-8'))]:
        if template.count(token)!=1:
            raise ValueError('Invalid build placeholder '+token)
        template=template.replace(token,value)
    notes=(root/'NOTES.md').read_text(encoding='utf-8')
    destination=resolve_output(root)
    destination.mkdir(parents=True,exist_ok=True)
    (destination/'index.html').write_text(template,encoding='utf-8',newline='\n')
    for name in ('data.json','atlas-submission.json'):
        shutil.copyfile(root/name,destination/name)
    shutil.copytree(root/'snapshots',destination/'snapshots',dirs_exist_ok=True)
    notes_html='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Codex compilation notes</title><style>body{font:16px/1.6 system-ui;max-width:900px;padding:2rem;margin:auto}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit}a{color:#2157a0}</style><a href="index.html">Back to the observatory</a><pre>'+html.escape(notes)+'</pre></html>'
    (destination/'notes.html').write_text(notes_html,encoding='utf-8')
    return destination, data

if __name__=='__main__':
    try:
        destination,data=build()
        print(f'Built {destination}: {len(data["models"])} models, {len(data["records"])} source observations.')
    except (ValueError,OSError) as error:
        sys.exit('Build failed: '+str(error))
