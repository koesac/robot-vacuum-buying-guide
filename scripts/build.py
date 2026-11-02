import json, re, pathlib
root = pathlib.Path(__file__).resolve().parents[1]
research = json.loads((root / 'data/research.json').read_text())
columns = research['columns']
models = [dict(zip(columns, row)) for row in research['models']]
assert research['schemaVersion'] == 1
assert all(len(row) == len(columns) for row in research['models'])
assert len({m['id'] for m in models}) == len(models)
assert all(m['price'] is None or m['price'] >= 0 for m in models)
page = (root / 'index.html').read_text()
bootstrap = "const response=await fetch('./data/research.json');if(!response.ok)throw new Error('Research data could not be loaded');const research=await response.json();const data=research.models.map(row=>Object.fromEntries(research.columns.map((key,i)=>[key,row[i]])));"
page, count = re.subn(r'const data=\[.*?\];(?=const \$)', lambda _: bootstrap, page, count=1, flags=re.S)
assert count == 1, 'Expected legacy inline model list; template changed'
page = page.replace(".join('\n')", ".join('\\r\\n')")
page = page.replace('21 model records', f'{len(models)} model records')
page = page.replace('The 21 records', f'The {len(models)} records')
page = page.replace(' / 21 models', ' / ${data.length} models')
page = page.replace('<option>Basic pad</option>', '<option>Basic pad</option><option>Vibrating pad</option><option>None</option>')
page = page.replace('<option>Manual</option>', '<option value="Manual">Charger-only / manual emptying</option>')
page = page.replace("[d.shop,'UK listing']", "[d.shop,'UK listing'],[research.evidence[String(d.id)]?.source,'Research source']")
page = page.replace('<a href="#sources">Evidence</a>', '<a href="#sources">Evidence</a><a href="./data/research.json">Research JSON</a>')
page = page.replace('No fresh product verification was performed for this update.', 'Five charger-only candidates have new source checks; older model records retain their previous caveats.')
page = page.replace('<script>\n', '<script>\n(async()=>{\n', 1)
page = page.replace('</script>', "\n})().catch(error=>{document.getElementById('count').textContent='Unable to load research data. Reload the page or check the Research JSON link.';console.error(error);});\n</script>", 1)
out = root / '_site'
(out / 'data').mkdir(parents=True, exist_ok=True)
(out / 'index.html').write_text(page)
(out / 'data/research.json').write_text(json.dumps(research, ensure_ascii=False, indent=2))
(out / '.nojekyll').touch()
print(f'Built {len(models)} models from data/research.json')
