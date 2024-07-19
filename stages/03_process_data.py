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

for file in files:

    out_basename = re.sub(extensions_re, '.parquet', file.name )
    out_file = brick_dir / file.relative_to('download').with_name( out_basename )

    if file.match('*.ism'):

        try:
            protein_dir = str(file).split('/')[1]

            names = {
              0: 'SMILES',
              1: 'DAT',   # TODO: Figure out what this column is
              2: 'Inhibition Metric',
              3: 'Relation',
              4: 'Value',
              5: 'Unit',
              6: 'Unknown', # TODO: Figure out what this column is
              7: 'Number of Decoys',
              8: 'SWISS PROT',
              9: 'Protein'
            }

            df = pd.read_csv(file, sep='\0', header=None)
            transformed_df = df[0].str.split(' ', n=9, expand=True)
            transformed_df.columns = list(names.values())
            protein_dir = pathlib.Path('brick/%s' % protein_dir)
            protein_dir.mkdir(exist_ok=True)
            transformed_df.to_parquet(out_file)
        except Exception as e:
          print ("File Not Processed: %s" % file)
    else:
      raise Exception('Unknown File Found: %s' % file)

