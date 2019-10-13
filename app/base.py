import requests
import json
import time
import sys
import argparse

alt_api_key = '9d2908c81003444ea908c81003b44ed4'
api_key = 'd522aa97197fd864d36b418f39ebb323'
url = 'https://api.weather.com'
deg_sym = chr(176)
latitude = longitude = 0


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
