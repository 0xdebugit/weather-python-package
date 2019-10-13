import requests
import json
import time
import sys
import argparse
import re

alt_api_key = '9d2908c81003444ea908c81003b44ed4'
api_key = 'd522aa97197fd864d36b418f39ebb323'
url = 'https://api.weather.com'
deg_sym = chr(176)
latitude = longitude = 0

# current info - default requested time info - daily
def basic_observation(latitude,longitude):
	print('[+] Daily Information')
	query = '{}/v2/turbo/vt1observation?apiKey={}&format=json&geocode={}%2C{}&language=en-IN&units=m'.
			format(url,api_key,latitude,longitude)
	basic_info = requests.get(query)
	basic_info = basic_info.content
	basic_info = json.loads(basic_info)['vt1observation']
	cur_date,cur_time,time_zone = re.split('[T +]',basic_info['observationTime'])
	res = ('\nObserved at : {} {} \nTemperature : {}, Feels like : {}, Desc : {}').format(cur_date,cur_time,
		str(basic_info['temperature'])+deg_sym,str(basic_info['feelsLike'])+deg_sym,basic_info['phrase'])
	return res

# get placeID - of city/state 
def start(place):
	print('[+] Fetching ID')
	query = '{}/v3/location/search?apiKey={}&format=json&language=en-IN&locationType=locale&query={}'.
			format(url,api_key,place)
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
	query = '{}/v3/location/point?apiKey={}&format=json&language=en-IN&placeid={}'.
			format(url,api_key,placeId)
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

	op = basic_observation(latitude,longitude)

	print(op)
