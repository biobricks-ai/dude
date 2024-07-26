# Imports
# -------
import os
import re
import pathlib
import pandas as pd

extensions = ['ism']
extensions_re = re.compile(r'\.(' + '|'.join(re.escape(ext) for ext in extensions) + r')$')
files = filter( lambda item: item.is_file(), pathlib.Path('download').rglob('*'))

brick_dir = pathlib.Path('brick')
brick_dir.mkdir(exist_ok=True)

for file in files:

    if os.stat(file).st_size == 0:
        continue

    out_basename = re.sub(extensions_re, '.parquet', file.name )
    out_file = brick_dir / file.relative_to('download').with_name( out_basename )

    if file.match('*scaffolds.ism'):
        protein_dir = str(file).split('/')[1]

        names = {
          0: 'SMILES',
        }

        df = pd.read_csv(file, sep='\0', header=None)
        transformed_df = df[0].str.split(' ', n=1, expand=True)

    elif file.match('*.ism'):

        protein_dir = str(file).split('/')[1]

        names = {
            0: 'SMILES',
            1: 'DAT',   # TODO: Figure out what this column is
            2: 'Inhibition_Metric',
            3: 'Relation',
            4: 'Value',
            5: 'Unit',
            6: 'Unknown', # TODO: Figure out what this column is
            7: 'Number_of_Decoys',
            8: 'SWISS_PROT',
            9: 'Protein'
        }

        df = pd.read_csv(file, sep='\0', header=None)
        transformed_df = df[0].str.split(' ', n=9, expand=True)

    else:
      raise Exception('Unknown File Found: %s' % file)

    transformed_df.columns = list(names.values())
    protein_dir = pathlib.Path('brick/%s' % protein_dir)
    protein_dir.mkdir(exist_ok=True)
    transformed_df.to_parquet(out_file)
