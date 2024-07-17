# Imports
# -------
import os
import urllib.request

os.makedirs('downloads', exist_ok=True)

data_links = {
  'dude_docking': 'https://dude.docking.org/db/subsets/all/all.tar.gz',
}

_ = [ urllib.request.urlretrieve(link, os.path.join('downloads', data)) for data, link in data_links.items() ]
