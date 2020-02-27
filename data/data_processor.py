import requests
import json
import googlemaps
  
print('Loading Data...')
with open('data.json') as json_file:
	data = json.load(json_file)

coordinates = {
	'schools': {},
	'current_cities': {},
	'hometowns': {}
}
raw_place_data = {
	'schools': {},
	'current_cities': {},
	'hometowns': {}
}
api_key = input('Enter Your API Key: ')
url = 'https://maps.googleapis.com/maps/api/geocode/json?'
gmaps = googlemaps.Client(key = api_key)

print('Fetching Location Data...')
for key in coordinates:
	for place in data['friend_places'][key]:
		if place != None:
			print('Fetching Location Data for ' + place + '...')
			res = gmaps.geocode(place)
			if len(res) > 0:
				coordinates[key][place] = res[0]['geometry']['location']
				coordinates[key][place]['people'] = data['friend_places'][key][place]
				raw_place_data[key][place] = res[0]
				print(raw_place_data[key][place])
  
print('Saving Data...')
with open('coordinate_data.json', 'w') as outfile:
		json.dump(coordinates, outfile)

with open('raw_places_data.json', 'w') as outfile:
		json.dump(raw_place_data, outfile)