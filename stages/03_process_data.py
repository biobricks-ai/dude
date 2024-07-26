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

    protein_dir = str(file).split('/')[1]

    if file.match('*scaffolds.ism'):

        names = {
          0: 'SMILES',
        }

        col_nums = 1
        df = pd.read_csv(file, sep='\0', header=None)

    elif file.match('actives_final.ism'):

        names = {
            0: 'SMILES',
            1: 'DAT',   # TODO: Figure out what this column is
            2: 'CHEMBL',   # TODO: Figure out what this column is
        }

        col_nums = 3
        df = pd.read_csv(file, sep='\0', header=None)

    elif file.match('decoys_scaffolds*') or file.match('decoys_final*'):

        names = {
          0: 'SMILES',
          1: 'DAT',   # TODO: Figure out what this column is
        }

        col_nums = 2
        df = pd.read_csv(file, sep='\0', header=None)

    elif file.match('decoys_tabbed*'):

        names = {
          0: 'SMILES',
          1: 'DAT',   # TODO: Figure out what this column is
        }

        col_nums = 2
        df = pd.read_csv(file, sep='\s+', header=None)

        continue # TODO: Process file into parquet Read columns correct with separator for transformed DF

    elif file.match('*murcko_enumeration.ism'):

        names = {
          0: 'SMILES',
          1: 'DAT',   # TODO: Figure out what this column is
          2: 'Inhibition_Metric',
          3: 'Relation',
          4: 'Value',
          5: 'Unit',
          6: 'Unknown', # TODO: Figure out what this column is
          7: 'Unknown 2', # TODO: Figure out what this column is
          8: 'SWISS_PROT',
          9: 'Protien',
          10: 'Number_of_Decoys',
        }
        col_nums = 10
        df = pd.read_csv(file, sep='\0', header=None)

    elif file.match('*.ism'):

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
        col_nums = 9
        df = pd.read_csv(file, sep='\0', header=None)

    else:
      raise Exception('Unknown File Found: %s' % file)

    transformed_df = df[0].str.split(' ', n=col_nums, expand=True)
    transformed_df.columns = list(names.values())
    protein_dir = pathlib.Path('brick/%s' % protein_dir)
    protein_dir.mkdir(exist_ok=True)
    transformed_df.to_parquet(out_file)
