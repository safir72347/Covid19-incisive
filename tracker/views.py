from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
import socket
import geoip2.database
import requests
from bs4 import BeautifulSoup
from bokeh.plotting import figure, output_file, show
from brokeh.embed import components

# Create your views here.

def index(request):

	#Get IP of Client
	ip = visitor_ip_address(request)
	print("IP : ",ip)

	#Check if IP is valid
	try:
		socket.inet_aton(ip)
		ip_valid = True
	except socket.error:
		ip_valid = False
	print(ip_valid)

	# Geo Location of IP
	ip = '49.35.96.81' #Temporary Ip since the Application is running on Local Host
	reader = geoip2.database.Reader('static/GeoIP/GeoLite2-City_20200814/GeoLite2-City.mmdb')

	response = reader.city(ip)

	#print(response.country.iso_code)
	#print(response.country.name)
	#print(response.country.names['zh-CN'])
	#print(response.subdivisions.most_specific.name)
	#print(response.subdivisions.most_specific.iso_code)
	#print(response.city.name)
	#print(response.postal.code)
	#print(response.location.latitude)
	#print(response.location.longitude)

	user_location = [response.city.name, response.postal.code, response.subdivisions.most_specific.name, response.country.name]
	
	print(user_location)

	city = response.city.name
	postal = response.postal.code
	state = response.subdivisions.most_specific.name
	country = response.country.name
	
	reader.close()

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

	state_data_list = []

	states_data = soup.find_all('div', class_='field-collection-item-field-covid-statewise-data')
	for s in states_data:
		#print(s.get_text())
		splitted_data = s.get_text().split(":")
		#state_data_list.append(splitted_data)
		state_name = str(splitted_data[1].split("Total")[0].lstrip())
		state_total = str(splitted_data[2].split("Cured")[0].lstrip())
		state_cured = str(splitted_data[3].split("Death")[0].lstrip())
		state_death = str(splitted_data[4].split("State")[0].lstrip())
		state_ongoing = str(int(state_total) - int(state_cured) + int(state_death))
		single_state = {"state_name":state_name, "state_total":state_total, "state_cured": state_cured, "state_death": state_death, "state_ongoing": state_ongoing}
		state_data_list.append(single_state)

	#print(state_data_list)
	
	for i in state_data_list:
		if i['state_name'].replace(" ", "") == state.replace(" ", ""):
			location_cases = i
			break
	location_details = {'ip':ip, 'city': city, 'postal': postal, 'state': state, 'country': country}

	p = figure(plot_width=400, plot_height=400)

	# add a circle renderer with a size, color, and alpha
	p.circle([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], size=20, color="navy", alpha=0.5)

	script, div = components(p)
	context = {'location_details':location_details, 'location_cases':location_cases, 'state_data':state_data_list, 'script':script, 'div':div}
	return render(request, 'index.html', context)

def visitor_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip