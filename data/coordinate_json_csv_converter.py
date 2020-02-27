import json 
import csv 
  
print('Loading JSON File...')
with open('coordinate_data.json', encoding = 'utf-8') as json_file: 
    data = json.load(json_file) 

for key in data:
	locations = {}

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
  
# schools_data = data['schools']
# current_cities_data = data['current_cities']
# hometowns_data = data['hometowns']
  
# schools_data_file = open('coordinate_schools_data_csv.csv', 'w') 
# csv_writer = csv.writer(schools_data_file) 
  
# print('Converting JSON Data to CSV for Schools...')
# count = 0  
# for school in schools_data: 
#     if count == 0: 
#         header = ['name'] + list(schools_data[school].keys())
#         csv_writer.writerow(header) 
#         count += 1
  
#     row = [school, schools_data[school]['lat'], schools_data[school]['lng'], ', '.join(schools_data[school]['people'])]
#     csv_writer.writerow(row) 

# schools_data_file.close() 

# cities_data_file = open('coordinate_cities_data_csv.csv', 'w') 
# csv_writer = csv.writer(cities_data_file) 
  
# print('Converting JSON Data to CSV for Cities...')
# count = 0  
# for city in current_cities_data: 
#     if count == 0: 
#         header = ['name'] + list(current_cities_data[city].keys())
#         csv_writer.writerow(header) 
#         count += 1
  
#     row = [city, current_cities_data[city]['lat'], current_cities_data[city]['lng'], ', '.join(current_cities_data[city]['people'])]
#     csv_writer.writerow(row) 
  
# print('Converting JSON Data to CSV for Cities...')
# count = 0  
# for city in hometowns_data: 
#     if count == 0: 
#         header = ['name'] + list(hometowns_data[city].keys())
#         csv_writer.writerow(header) 
#         count += 1
  
#     row = [city, hometowns_data[city]['lat'], hometowns_data[city]['lng'], ', '.join(hometowns_data[city]['people'])]
#     csv_writer.writerow(row) 
  
# cities_data_file.close() 