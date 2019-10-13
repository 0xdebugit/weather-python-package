import requests
import json
import time
import sys
from bs4 import BeautifulSoup
import argparse
import re

alt_api_key = '9d2908c81003444ea908c81003b44ed4'
api_key = 'd522aa97197fd864d36b418f39ebb323'
url = 'https://api.weather.com'
deg_sym = chr(176)
latitude = longitude = 0

start_time = time.time()

if sys.version_info[0] < 3:
	raise Exception("Must be using Python 3")

# current info - default requested time info - daily
def basic_observation(latitude,longitude):
	print('[+] Daily Information')
	query = '{}/v2/turbo/vt1observation?apiKey={}&format=json&geocode={}%2C{}&language=en-IN&units=m'.format(url,api_key,
		latitude,longitude)
	basic_info = requests.get(query)
	basic_info = basic_info.content
	basic_info = json.loads(basic_info)['vt1observation']
	cur_date,cur_time,time_zone = re.split('[T +]',basic_info['observationTime'])
	res = ('\nObserved at : {} {} \nTemperature : {}, Feels like : {}, Desc : {}').format(cur_date,cur_time,
		str(basic_info['temperature'])+deg_sym,str(basic_info['feelsLike'])+deg_sym,basic_info['phrase'])
	return res

# info - monthly
def forecast(latitude,longitude):
	res = '' 
	query = '{}/v2/turbo/vt1dailyForecast?apiKey={}&format=json&geocode={}%2C{}&language=en-IN&units=m'.format(url,
		api_key,latitude,longitude)
	forecast_info = requests.get(query)
	forecast_info_raw = forecast_info.content
	forecast_info = json.loads(forecast_info_raw)['vt1dailyForecast']
	forecast_info_day = json.loads(forecast_info_raw)['vt1dailyForecast']['day']
	forecast_info_night = json.loads(forecast_info_raw)['vt1dailyForecast']['night']
	json_dates = forecast_info['validDate']
	json_day_phrase = forecast_info_day['phrase']
	json_night_phrase = forecast_info_night['phrase']
	json_day_temp = forecast_info_day['temperature']
	json_night_temp = forecast_info_night['temperature']

	for i in range(len(json_dates)):
		if i == 0:
			res += '-'*80+'\n'
			res += ('{:<15}{:<5}{:<25}{:<5}{:<5}\n'.format('Date','Temp','Day','Temp','Night'))
			res += '-'*80+'\n'
		else:
			res += ('{:<15}{:<5}{:<25}{:<5}{:<5}\n'.format(json_dates[i][:10],str(json_day_temp[i])+deg_sym,
				str(json_day_phrase[i]),str(json_night_temp[i])+deg_sym,json_night_phrase[i]))
	return res

# info - hourly
def hourly(placeid):
	query = 'https://weather.com/en-IN/weather/hourbyhour/l/{}'.format(placeid)
	res = requests.get(query)
	hourly = res.content
	soup = BeautifulSoup(hourly,'lxml')
	table = soup.find(class_="twc-table")
	hourlydata = []
	val = resp = ''

	cnt = 0
	for my_table in table:
		rows = my_table.find_all('tr', recursive=False)                
		for row in rows:
			hourlydata.append([])
			cells = row.find_all(['th', 'td'])        
			#  print(cells)
			for cell in cells:
				if(cell.find('span') is not None):
					#  print(cell.find('span').text)
					#  print(cnt)
					val = cell.find('span').text.strip()
					if val == '':
						hourlydata[cnt].append('0')
					else:
						hourlydata[cnt].append(val)
			cnt += 1
	hourlydata.pop(0)
	cnt = 0
	for i in hourlydata:
		if cnt == 0:
			resp += '-'*80+'\n'
			resp += ('{:<15}{:<25}{:<15}{:<15}\n'.format('Time','Description','Temp','Feels like'))
			resp += '-'*80+'\n'
		else:
			resp += ('{:<15}{:<25}{:<15}{:<15}\n'.format(i[0],i[1],i[2],i[3]))
		cnt +=1
	return resp

# get placeID - of city/state 
def start(place):
	print('[+] Fetching ID')
	query = '{}/v3/location/search?apiKey={}&format=json&language=en-IN&locationType=locale&query={}'.format(url,
		api_key,place)
	res = requests.get(query)
	resp = res.content
	if(res.status_code == 404):
		sys.exit('Invalid Place or Couldnt reach the server')
	else:
		json_decoded = json.loads(resp)['location']
		placeId = json_decoded['placeId'][0]
	return placeId

# get gelocation - latitude & longitude
def long_lat(placeId):
	print('[+] Fetching longitude & latitude Info')
	query = '{}/v3/location/point?apiKey={}&format=json&language=en-IN&placeid={}'.format(url,api_key,placeId)
	res = requests.get(query)
	resp = res.content
	latitude = json.loads(resp)['location']['latitude']
	longitude = json.loads(resp)['location']['longitude']
	return ({'latitude' : latitude, 'longitude' : longitude})

# display if any error message
def parser_error(errmsg):
	print("Usage: python " + sys.argv[0] + " [Options] use -h for help")
	sys.exit()

# parse the arguements
def parse_args():
	parser = argparse.ArgumentParser(epilog='\tExample: \r\npython ' + sys.argv[0] + " --place bengaluru --fc_type daily")
	parser._optionals.title = "OPTIONS"
	parser.error = parser_error
	parser.add_argument('--place',default='bengaluru', type=str, help='Enter a valid city/state name')
	parser.add_argument('--fc_type',default='daily',type=str, help='daily or monthly or hourly')
	args = parser.parse_args()
	return args



if __name__ == "__main__":
	args = parse_args()
	place = args.place
	fc_type = args.fc_type

	_placeid = start(place)
	data = long_lat(_placeid)
	latitude = data['latitude']
	longitude = data['longitude']

	print('[+] '+place+' [+] '+fc_type)
	if(fc_type == 'daily'):
		op = basic_observation(latitude,longitude)
	elif(fc_type == 'monthly'):
		op = forecast(latitude,longitude)
	elif(fc_type == 'hourly'):
		op = hourly(_placeid)
	else:
		sys.exit('Sorry this forecast type is not available')

	print(op)
