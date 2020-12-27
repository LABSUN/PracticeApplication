from datetime import datetime
import pytz
import requests
import pycountry
from flask import request, redirect
from geopy.geocoders import Nominatim


city = "Los Angeles"

url = f'http://api.weatherapi.com/v1/current.json?key=72a80a39b287444d9e0234203202512&q={city}'
print(url)
res = requests.get(url)


data = res.json()



country_code_data =  pycountry.countries.search_fuzzy(data['location']['country'])
country_code = list(country_code_data)[0]
country_alpha = country_code.alpha_2
temp = data["current"]['temp_f']
tz_id = pytz.timezone(data['location']['tz_id']) 
time = datetime.now(tz_id)
timefinal = time.strftime("%I:%M %p")
country = data['location']['country']

flag_link = f"https://www.countryflags.io/{country_alpha}/flat/64.png"
region = data["location"]["region"]
lat = data["location"]["lat"]
lon = data["location"]["lon"]

weathertype = data["current"]['condition']['text']
weathericon = data["current"]['condition']['icon']

print(region)
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def hello_world():
	title="Weather | Homepage"
	return render_template("index.html", temp=temp, city = city, time = timefinal, country = country, flag = flag_link, degree = "Farenheit", region = region, lat = lat, lon = lon, weathertype = weathertype, weathericon = weathericon)

@app.route('/city', methods = ['POST'])
def signup():
	cityreq = request.form['city']
	if cityreq.capitalize() == "Pyongyang":
		return render_template("fail.html")

	time = datetime.now()

	current_time = time.strftime("%H:%M:%S")
	print(cityreq)
	city = cityreq
	url = f'http://api.weatherapi.com/v1/current.json?key=72a80a39b287444d9e0234203202512&q={city}'
	print(url)
	res = requests.get(url)

	data = res.json()

	if data.get('current')==None: 
		return render_template("fail.html")

	

	tempcheck = request.form['temp']
	print(tempcheck)
	degreetype = ""
	if tempcheck == "f":
		temp = data["current"]['temp_f']
		degreetype = "Farenheit"
	elif tempcheck == "c":
		temp = data["current"]['temp_c']
		degreetype = "Celcius"
	else:
		temp1 = data["current"]['temp_c'] + 273.15
		temp = round(temp1,1)
		degreetype = "Kelvin"	

	country = data['location']['country']
	country_code_data =  pycountry.countries.search_fuzzy(data['location']['country'])
	country_code = list(country_code_data)[0]
	country_alpha = country_code.alpha_2

	flag_link = f"https://www.countryflags.io/{country_alpha}/flat/64.png"
	lat = data["location"]["lat"]
	lon = data["location"]["lon"]
	tz_id = pytz.timezone(data['location']['tz_id']) 
	time = datetime.now(tz_id)
	timefinal = time.strftime("%I:%M %p")
	cityfinal = data["location"]["name"]
	region = data["location"]["region"]
	weathertype = data["current"]["condition"]["text"]
	weathericon = data["current"]["condition"]["icon"]
	return render_template("index.html", temp=temp, city = cityfinal, time = timefinal , country = country, flag = flag_link, region=region, degree = degreetype, lat = lat, lon = lon, weathertype = weathertype, weathericon = weathericon)

	if __name__ == "__main__":
		app.run(debug=True)