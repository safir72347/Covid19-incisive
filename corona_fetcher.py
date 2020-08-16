import requests
from bs4 import BeautifulSoup

url = "https://www.mygov.in/corona-data/covid19-statewise-status/"

r = requests.get(url)
htmlContent = r.content
soup = BeautifulSoup(htmlContent, 'html.parser')

class_names = ['field-name-field-covid-india-as-on' ,'field-name-field-passenger-screened-format', 'field-name-field-total-active-case', 
'field-name-field-total-cured-discharged', 'field-name-field-migrated-counts', 'field-name-field-total-death-case', 
'field-name-field-last-total-active', 'field-name-field-last-total-cured', 'field-name-field-last-total-death', 
'field-name-field-total-samples-tested', 'field-name-field-samples-tested-today', 'field-name-field-last-sample-tested-date']


for classes in class_names:
	print(soup.find('div', class_=classes).get_text())
	
'''
all_states = soup.find_all('div', class_="field-item even")
for state in all_states:
	print(state.string)
'''

state_data_list = []

states_data = soup.find_all('div', class_='field-collection-item-field-covid-statewise-data')
for s in states_data:
	#print(s.get_text())
	splitted_data = s.get_text().split(":")
	#state_data_list.append(splitted_data)
	state_name = splitted_data[1].split("Total")[0].lstrip()
	state_total = splitted_data[2].split("Cured")[0].lstrip()
	state_cured = splitted_data[3].split("Death")[0].lstrip()
	state_death = splitted_data[4].split("State")[0].lstrip()
	state_ongoing = str(int(state_total) - int(state_cured) + int(state_death))
	single_state = [state_name, state_total, state_cured, state_death, state_ongoing]
	state_data_list.append(single_state)

print(state_data_list)
