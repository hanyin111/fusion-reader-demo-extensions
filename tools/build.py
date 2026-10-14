from pathlib import Path
import hashlib
import json
import shutil

root = Path(__file__).resolve().parents[1]
out = root / 'site'
(out / 'scripts').mkdir(parents=True, exist_ok=True)
source = (root / 'sources/fusiondemo.js').read_bytes()
digest = hashlib.sha256(source).hexdigest()
name = f'fusiondemo-{digest}.js'
(out / 'scripts' / name).write_bytes(source)
entry = dict(package='fusiondemo', name='聚阅原创阅读演示', version='v1.0.0', type='novel',
             lang='zh', author='聚阅演示', nsfw=False, url=f'scripts/{name}',
             size=len(source), sha256=digest, minAppVersion='1.4.0')
manifest = dict(schemaVersion=1, name='聚阅原创演示仓库',
                website='https://hanyin111.github.io/fusion-reader-demo-extensions/', extensions=[entry])
(out / 'index.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
shutil.copytree(root / 'public', out, dirs_exist_ok=True)
shutil.copy2(root / 'LICENSE', out / 'LICENSE')
(out / '.nojekyll').touch()
print('Built one demo source, three original novels, nine chapters.')
