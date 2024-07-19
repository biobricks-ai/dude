# Imports
# -------
import urllib.request
from bs4 import BeautifulSoup

dude_target_page = urllib.request.urlopen("https://dude.docking.org/targets")
dude_target_page = dude_target_page.read().decode('utf-8')

soup = BeautifulSoup(dude_target_page, 'lxml')
target_table = soup.find('table')
rows = target_table.findAll('tr')

active_base_url = 'https://dude.docking.org//targets/PROTEIN/actives_nM_combined.ism\n'
inactive_base_url = 'https://dude.docking.org//targets/PROTEIN/inactives_nM_combined.ism\n'

links_text = open('links.txt', 'w')

for row in rows:
    cols = row.find_all('td')
    if cols:
        protein_target = cols[1].get_text().lower()

        active_url = active_base_url.replace('PROTEIN', protein_target)
        inactive_url = inactive_base_url.replace('PROTEIN', protein_target)

        links_text.write('-O ' + protein_target + '.ism' + ' ' + active_url)
        links_text.write('-O ' + protein_target + '.ism' + ' ' + inactive_url)
