# Imports
# -------
import re
import pathlib
import pandas as pd

extensions = ['ism']
extensions_re = re.compile(r'\.(' + '|'.join(re.escape(ext) for ext in extensions) + r')$')

files = filter( lambda item: item.is_file(), pathlib.Path('download').rglob('*') )

brick_dir = pathlib.Path('brick')
brick_dir.mkdir(exist_ok=True)

for file in files:
  out_basename = re.sub(extensions_re, '.parquet', file.name )
  out_file = brick_dir / file.relative_to('download').with_name( out_basename )

  if file.match('*.ism'):
    df = pd.read_csv(file, header=None, names=['SMILES', 'dat', 'inhibition', 'X', 'XX', 'Protein'], sep='\t')
    print (df)
    # df.to_parquet(out_file)

  else:
    raise Exception('Unknown File Found: %s' % file)
