from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
import socket
import geoip2.database


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
	reader.close()
	print(user_location)
	return render(request, 'index.html')

def visitor_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip