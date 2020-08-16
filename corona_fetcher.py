import requests
from bs4 import BeautifulSoup

url = "https://www.mygov.in/corona-data/covid19-statewise-status/"

r = requests.get(url)
htmlContent = r.content
soup = BeautifulSoup(htmlContent, 'html.parser')

class_names = ['field-name-field-passenger-screened-format', 'field-name-field-total-active-case', 'field-name-field-total-cured-discharged', 'field-name-field-migrated-counts', 'field-name-field-total-death-case', 'field-name-field-last-total-active', 'field-name-field-last-total-cured', 'field-name-field-last-total-death', 'field-name-field-total-samples-tested', 'field-name-field-samples-tested-today']

for classes in class_names:
	print(soup.find('div', class_=classes).get_text())