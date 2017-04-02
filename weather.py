import requests
import xml.etree.ElementTree as ET 

DEBUG = 0

# Rain forecast
def get_nowcast_for_location(latitude, longditude):  

	parameters = {"lat": latitude, "lon": longditude} 

	# Read XML data from URL
	response = requests.get("http://api.met.no/weatherapi/nowcast/0.9/", params=parameters)

	if DEBUG:
		print(response.status_code) # (200 - OK)

	# Root element in xml tree
	weather_data_root = ET.fromstring(response.content) 

	return weather_data_root



def get_time_steps_from_weather_data(weater_data_root):

	# Product - the node in the xml tree that contains the nowcast data at continuous time steps with 8 minutes intervals
	product = weather_data_root.find('product')

	time_steps = product.findall('time')

	return time_steps




def get_max_precipitation_from_weather_data(weather_data_root):

	max_precipitation = 0

	time_steps = get_time_steps_from_weather_data(weather_data_root)

	for time_step in time_steps:

		if DEBUG:
			print time_step.tag, time_step.attrib
		
		locations = time_step.findall('location')

		for location in locations:
			precipitation = location.find('precipitation')

			precipitation = float(precipitation.get('value'))
			
			max_precipitation = max(precipitation, max_precipitation)


	return max_precipitation


def get_wind_speed_from_weather_data(weather_data_root):
	
	wind_speed = 0

	time_steps = get_time_steps_from_weather_data(weather_data_root)

	for time_step in time_steps:
		
		locations = time_step.findall('location') 

		for location in locations:
			wind_gust = location.find('windGust')		

			wind_speed = float(wind_gust.get('mps'))
	
	return wind_speed


def need_umbrella(precipitation, threshold=1):

	if precipitation >= threshold:
		return True
	
	return False


def print_message_for_precipitation(precipitation):

	print "Maximum precipitation expected for the next two hours:", precipitation, "mm/h."

	if need_umbrella(precipitation, threshold=0.5):
		print "You need to bring an umbrella!"
	else:
		print "There is no need for an umbrella, at least for the next two hours  #Trondheim "


weather_data_root = get_nowcast_for_location(63.42, 10.36) # location for Ila, Trondheim

max_precipitation = get_max_precipitation_from_weather_data(weather_data_root)


print_message_for_precipitation(max_precipitation)

