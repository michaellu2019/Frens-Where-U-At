import json 
import csv 
  
print('Loading JSON File...')
with open('coordinate_data.json', encoding = 'utf-8') as json_file: 
    data = json.load(json_file) 

for key in data:
	locations = {}

	# merge all data for repeated locations
	for place in data[key]:
		loc = (data[key][place]['lat'], data[key][place]['lng'])
		if loc in locations:
			data[key][locations[loc]]['people'] += ', '.join(data[key][place]['people'])
			data[key][place] = {}
		else:
			data[key][place]['people'] = ', '.join(data[key][place]['people'])
			locations[loc] = place

with open('coordinate_data_to_convert.json', 'w') as outfile:
		json.dump(data, outfile)