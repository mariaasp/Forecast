import requests
import xml.etree.ElementTree as ET 

DEBUG = 0


def get_nowcast_for_location(latitude, longditude):  

	parameters = {"lat": latitude, "lon": longditude} 

	# Read XML data from URL
	response = requests.get("http://api.met.no/weatherapi/nowcast/0.9/", params=parameters)

	if DEBUG:
		print(response.status_code) # (200 - OK)

	# Root element in xml tree
	root = ET.fromstring(response.content) 

	return root


def get_max_precipitation(root):

	unit 			  = None
	max_precipitation = 0

	# Traverse the xml tree
	# Product - the node in the xml tree that contains the nowcast data at continuous time steps with 8 minutes intervals
	product = root.find('product')
	
	time_steps = product.findall('time')

	for time_step in time_steps:

		if DEBUG:
			print time_step.tag, time_step.attrib
		
		locations = time_step.findall('location')

		for location in locations:
			precipitation = location.find('precipitation')

			unit  		  = precipitation.get('unit')
			precipitation = float(precipitation.get('value'))

			if precipitation > max_precipitation:
				max_precipitation = precipitation

	return max_precipitation, unit



def need_umbrella(precipitation, threshold=1):

	if precipitation >= threshold:
		return True
	
	return False


root = get_nowcast_for_location(63.42, 10.36) # location for Ila, Trondheim
max_precipitation, unit = get_max_precipitation(root)

print "Maximum precipitation expected for the next 2 hours:", max_precipitation, unit 

if need_umbrella(max_precipitation, threshold=0.5):
	print "You need to bring an umbrella!"
else:
	print "There is no need for an umbrella, at least for the next two hours  #Trondheim "