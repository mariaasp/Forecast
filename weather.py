import requests
import xml.etree.ElementTree as ET 



def get_nowcast_for_location(latitude, longditude):  

	parameters = {"lat": latitude, "lon": longditude} 
	response = requests.get("http://api.met.no/weatherapi/nowcast/0.9/", params=parameters)

	# print(response.status_code) #prints status (200 - OK)

	root = ET.fromstring(response.content) # root element in xml tree

	return root


def get_max_precipitation(root):

	product = root.find('product')
	times = product.findall('time')
	max_precipitation = 0
	unit = None

	for time in times:
#		print time.tag, time.attrib
		
		locations = time.findall('location')
		for location in locations:
			precipitation = location.find('precipitation')
			value = float(precipitation.attrib['value'])
			unit = precipitation.attrib['unit']

			if value > max_precipitation:
				max_precipitation = value

	return max_precipitation, unit



def need_umbrella(precipitation, threshold=1):
	if precipitation >= threshold:
		return True
	return False


root = get_nowcast_for_location(63.42, 10.36) # location for Ila, Trondheim : lat: 63.42, long: 10.36
max_precipitation, unit = get_max_precipitation(root)

print "Maximum precipitation expected for the next 2 hours:", max_precipitation, unit 
if need_umbrella(max_precipitation, threshold=0.5):
	print "You need to bring an umbrella!"
else:
	print "There is no need for an umbrella, at least for the next two hours  #Trondheim "