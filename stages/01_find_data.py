# Imports
# -------
import os
import pandas as pd

os.makedirs('list', exist_ok=True)

url = 'https://dude.docking.org/targets'
df = pd.read_html(url)[0]
df['Target Name'].to_csv('list/target_links.txt', header=False, index=False)
