# Imports
# -------
import re
import pathlib
import pandas as pd

extensions = ['zip']
extensions_re = re.compile(r'\.(' + '|'.join(re.escape(ext) for ext in extensions) + r')$')
files = filter( lambda item: item.is_file(), pathlib.Path('download').rglob('*'))

brick_dir = pathlib.Path('brick')
brick_dir.mkdir(exist_ok=True)

smiles = []

for file in files:
  out_basename = re.sub(extensions_re, '.parquet', file.name )
  out_file = brick_dir / file.relative_to('download').with_name( out_basename )

  if file.match('*.ism'):

    lines = list(filter(None, open(file, 'r').read().split('\n')))
    for line in lines:
        if 'IC50' in line:
            inhibitor_value = line.split('IC50')[1].split(' ')[2]
        elif 'Ki' in line:
            inhibitor_value = line.split('Ki')[1].split(' ')[2]
        else:
            raise Exception('No Inhibition Value: %s' % line)

  else:
    raise Exception('Unknown File Found: %s' % file)
