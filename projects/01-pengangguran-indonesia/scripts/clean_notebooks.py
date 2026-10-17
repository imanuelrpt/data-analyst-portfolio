import json, glob

files = glob.glob('projects/01-pengangguran-indonesia/notebooks/*.ipynb')
for path in files:
    with open(path, encoding='utf-8') as f:
        nb = json.load(f)
    changed = False
    for cell in nb.get('cells', []):
        if cell.get('cell_type') == 'code':
            if cell.get('outputs'):
                cell['outputs'] = []
                changed = True
            if cell.get('execution_count') is not None:
                cell['execution_count'] = None
                changed = True
    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1)
            f.write('\n')
    print('cleaned' if changed else 'ok', path)
