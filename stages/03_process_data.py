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

smiles_list = []
inhibitor_constant_values = []
inhibitory_concentration_values = []
protein_targets = []
active_or_inactive = []

for file in files:
  out_basename = re.sub(extensions_re, '.parquet', file.name )
  out_file = brick_dir / file.relative_to('download').with_name( out_basename )

  if file.match('*.ism'):

      lines = list(filter(None, open(file, 'r').read().split('\n')))

      protein_target = file.name.split('_')[0]
      state = file.name.split('_')[1].split('.')[0]

      for line in lines:
          smiles = line[0]

          if 'IC50' in line:
              inhibitory_concentration_value = line.split('IC50')[1].split(' ')[2]
              inhibitor_constant_value = None
          elif 'Ki' in line:
              inhibitor_constant_value = line.split('Ki')[1].split(' ')[2]
              inhibitory_concentration_value = None
          else:
              raise Exception('No Inhibition Value: %s' % line)

          smiles_list.append(smiles)
          inhibitor_constant_values.append(inhibitor_constant_value)
          inhibitory_concentration_values.append(inhibitory_concentration_value)
          protein_targets.append(protein_target)
          active_or_inactive.append(state)
  else:
    raise Exception('Unknown File Found: %s' % file)

df = pd.DataFrame()

df['SMILES'] = smiles_list
df['KI'] = inhibitor_constant_values
df['IC50'] = inhibitory_concentration_values
df['Protein Target'] = protein_targets
df['State'] = active_or_inactive
