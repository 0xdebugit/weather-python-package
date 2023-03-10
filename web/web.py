from flask import Flask, render_template, request
import requests
import json
from bs4 import BeautifulSoup
import sys
import re

app = Flask(__name__)

alt_api_key = '9d2908c81003444ea908c81003b44ed4'
api_key = 'd522aa97197fd864d36b418f39ebb323'
url = 'https://api.weather.com'
deg_sym = chr(176)
latitude = longitude = 0
custom_info = {}

class cloud_weather:
	
	def __init__(self, place):
		self.place = place
		self.placeid = self.start(place)
		self.data = self.long_lat(self.placeid)
		self.latitude = self.data['latitude']
		self.longitude = self.data['longitude']

	# info - daily
	def daily(self):
		query = '{}/v2/turbo/vt1observation?apiKey={}&format=json&geocode={}%2C{}&language=en-IN&units=m'.format(
			 url, api_key, self.latitude, self.longitude)
		basic_info = requests.get(query)
		basic_info = basic_info.content
		basic_info = json.loads(basic_info)['vt1observation']
		cur_date, cur_time, time_zone = re.split('[T +]', basic_info['observationTime'])
		basic_info['address'] = custom_info['address']
		basic_info['temperature'] = str(basic_info['temperature'])+deg_sym
		basic_info['feelsLike'] = str(basic_info['feelsLike'])+deg_sym
		basic_info['observationTime'] = cur_time+' on '+cur_date
		return json.dumps(basic_info)

	# info - monthly
	def monthly(self):
		res = ''
		mylist = []
		query = '{}/v2/turbo/vt1dailyForecast?apiKey={}&format=json&geocode={}%2C{}&language=en-IN&units=m'.format(
				url, api_key, self.latitude, self.longitude)
		forecast_info = requests.get(query)
		forecast_info_raw = forecast_info.content
		forecast_info = json.loads(forecast_info_raw)['vt1dailyForecast']
		forecast_info_day = json.loads(forecast_info_raw)[
			'vt1dailyForecast']['day']
		forecast_info_night = json.loads(forecast_info_raw)[
			'vt1dailyForecast']['night']
		json_dates = forecast_info['validDate']
		json_day_phrase = forecast_info_day['phrase']
		json_night_phrase = forecast_info_night['phrase']
		json_day_temp = forecast_info_day['temperature']
		json_night_temp = forecast_info_night['temperature']

		for i in range(len(json_dates)):
			mylist.append([json_dates[i][:10],str(json_day_temp[i])+deg_sym,str(json_day_phrase[i]),str(json_night_temp[i])+deg_sym,str(json_night_phrase[i])])
		custom_info['monthly'] = mylist
		return json.dumps(custom_info)

	# info - hourly
	def hourly(self):
		query = 'https://weather.com/en-IN/weather/hourbyhour/l/{}'.format(
			self.placeid)
		res = requests.get(query)
		hourly = res.content
		soup = BeautifulSoup(hourly, 'lxml')
		table = soup.find(class_="twc-table")
		hourlydata = []
		val = resp = ''
		cnt = 0
		for my_table in table:
			rows = my_table.find_all('tr', recursive=False)
			for row in rows:
				hourlydata.append([])
				cells = row.find_all(['th', 'td'])
				for cell in cells:
					if(cell.find('span') is not None):
						val = cell.find('span').text.strip()
						if val == '':
							hourlydata[cnt].append('0')
						else:
							hourlydata[cnt].append(val)
				cnt += 1
		hourlydata.pop(0)
		custom_info['hourly'] = hourlydata
		return json.dumps(custom_info)

	# get placeID - of city/state
	def start(self, place):
		query = '{}/v3/location/search?apiKey={}&format=json&language=en-IN&locationType=locale&query={}'.format(url, api_key, place)
		res = requests.get(query)
		resp = res.content
		if(res.status_code == 404):
			sys.exit('Invalid Place or Couldnt reach the server')
		else:
			json_decoded = json.loads(resp)['location']
			placeId = json_decoded['placeId'][0]
			custom_info['address'] = json_decoded['address'][0]
			custom_info['placeid'] = placeId
		return placeId

	# get gelocation - latitude & longitude
	def long_lat(self, placeId):
		query = '{}/v3/location/point?apiKey={}&format=json&language=en-IN&placeid={}'.format(url, api_key, placeId)
		res = requests.get(query)
		resp = res.content
		latitude = json.loads(resp)['location']['latitude']
		longitude = json.loads(resp)['location']['longitude']
		return ({'latitude': latitude, 'longitude': longitude})




@app.route('/')
def index():
	return render_template('index.html')


@app.route('/daily', methods=['GET', 'POST'])
def dailyfn():
	reqplace = request.form['place']
	userreq = cloud_weather(reqplace)
	return userreq.daily()


@app.route('/hourly', methods=['GET', 'POST'])
def hourlyfn():
	reqplace = request.form['place']
	userreq = cloud_weather(reqplace)
	return userreq.hourly()

@app.route('/monthly', methods=['GET', 'POST'])
def monthlyfn():
	reqplace = request.form['place']
	userreq = cloud_weather(reqplace)
	return userreq.monthly()

if __name__ == "__main__":
	app.run(debug=True)