from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
import socket
import geoip2.database
import requests
from bs4 import BeautifulSoup

from plotly.offline import plot
import plotly.graph_objects as go

import json
import numpy as np
import pandas as pd
import plotly.express as px


import plotly.io as pio
pio.renderers.default = 'browser'

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

	texts = []
	for classes in class_names:
		temp = soup.find('div', class_=classes).get_text()
		texts.append(temp)

	state_data_list = []
	state_data_list1 = []

	states_data = soup.find_all('div', class_='field-collection-item-field-covid-statewise-data')
	for s in states_data:
		#print(s.get_text())
		splitted_data = s.get_text().split(":")
		#state_data_list.append(splitted_data)
		state_name = str(splitted_data[1].split("Total")[0].lstrip())
		state_total = int(splitted_data[2].split("Cured")[0].lstrip())
		state_cured = int(splitted_data[3].split("Death")[0].lstrip())
		state_death = int(splitted_data[4].split("State")[0].lstrip())
		state_ongoing = int(int(state_total) - int(state_cured) + int(state_death))
		
		
		if state_name == "Andaman and Nicobar":
			state_name = "Andaman & Nicobar Island"
		if state_name == "Dadra and Nagar Haveli and Daman and Diu":
			state_name = "Dadara & Nagar Havelli"
			single_state = {"state_name":state_name, "state_total":state_total, "state_cured": state_cured, "state_death": state_death, "state_ongoing": state_ongoing}
			single_state1 = [state_name, state_total, state_cured, state_death, state_ongoing]
			state_name = "Daman & Diu"
		if state_name == "Jammu and Kashmir":
			state_name = "Jammu & Kashmir"
		if state_name == "Arunachal Pradesh":
			state_name = "Arunanchal Pradesh"
		if state_name == "Delhi":
			state_name = "NCT of Delhi"
		if state_name == "Telengana":
			state_name = "Telangana"

		single_state = {"state_name":state_name, "state_total":state_total, "state_cured": state_cured, "state_death": state_death, "state_ongoing": state_ongoing}
		single_state1 = [state_name, state_total, state_cured, state_death, state_ongoing]
		state_data_list.append(single_state)
		if state_name!="Ladakh":
			state_data_list1.append(single_state1)

	#print(state_data_list)
	
	for i in state_data_list:
		if i['state_name'].replace(" ", "") == state.replace(" ", ""):
			location_cases = i
			break
	location_details = {'ip':ip, 'city': city, 'postal': postal, 'state': state, 'country': country}

	india_states = json.load(open("static/plotly_mapping/states_india.geojson", "r"))
	state_id_map = {}
	#print(india_states['features'])
	for feature in india_states["features"]:
		feature["id"] = feature["properties"]["state_code"]
		state_id_map[feature["properties"]["st_nm"]] = feature["id"]
	#print(state_id_map)


	df = pd.DataFrame(state_data_list1, columns=['State or union territory', 'Total', 'Cured', 'Deaths', 'OnGoing'])
	#print(df)
	df['cases'] = df['OnGoing']
	df["id"] = df["State or union territory"].apply(lambda x: state_id_map[x])
	df['cases_scale'] = np.log10(df["cases"])
	
	
	fig = px.choropleth(
		df,
		locations="id",
		geojson=india_states,
		color="cases_scale",
		color_continuous_scale="Viridis",
		hover_name="State or union territory",
		hover_data=["cases"],
		title="Corona Cases in India",
	)
	fig.update_geos(fitbounds="locations", visible=False)
	fig.update_layout(margin=dict(l=0, r=0, t=25, b=0))
	#fig.show()
	plot_div = plot(fig, output_type='div', include_plotlyjs=True)
	fig = px.choropleth_mapbox(
		df,
		locations="id",
		geojson=india_states,
		color="cases_scale",
		hover_name="State or union territory",
		hover_data=["cases"],
		title="Corona Cases in India",
		mapbox_style="carto-positron",
		center={"lat": 24, "lon": 78},
		zoom=3,
		opacity=0.5,
	)
	fig.update_geos(fitbounds="locations", visible=False)
	fig.update_layout(margin=dict(l=0, r=0, t=25, b=0))
	#fig.show()

	plot_div1 = plot(fig, output_type='div', include_plotlyjs=False)



	x1 = [i[4] for i in state_data_list1]
	y1 = [i[4] for i in state_data_list1]

	trace = go.Scatter(
		x = x1,
		y = y1
	)
	layout = dict(
		title = 'OnGoing Cases Vs Cured cases',
		xaxis = dict(range=[min(x1),max(x1)]),
		yaxis = dict(range=[min(y1),max(y1)])
	)
	fig = go.Figure(data=[trace], layout=layout)
	plot_div2 = plot(fig, output_type='div', include_plotlyjs=False)
	

	context = {'texts':texts,'location_details':location_details, 'location_cases':location_cases, 'state_data':state_data_list, 'plot': plot_div, 'plot1': plot_div1, 'plot2':plot_div2}
	return render(request, 'index.html', context)

def visitor_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip