from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from random import random
import json
import getpass

# get user credentials
# username = 'SibeliusTheMessenger@gmail.com'
# password = 'GNSConfessions'
username = input('Enter your Facebook Username: ')
password = getpass.getpass('Enter your Facebook Password: ')

# login to facebook and go to friends page
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome('chromedriver.exe', chrome_options = chrome_options)
driver.get('http://facebook.com')

driver.find_element_by_id('email').send_keys(username)
driver.find_element_by_id('pass').send_keys(password)
driver.find_element_by_id('loginbutton').click()
# driver.find_element_by_xpath("//button[@name='login']").click()
print('Logging In...')
# sleep(random() * 5.2 + 5.7)

resart = False
if resart:
	# navigate to profile and friends list
	profile_button = WebDriverWait(driver, 12).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a._2s25')))
	profile_button.click()
	print('Going to Profile...')
	sleep(random() * 3.3 + 4.6)

	driver.get(driver.current_url + '/friends')
	friends_button = WebDriverWait(driver, 12).until(EC.element_to_be_clickable((By.XPATH, "//a[@class='_6-6'][@data-tab-key='friends']")))
	friends_button.click()
	print('Going to Friends List...')

	# get all the URLs of friends
	scroll_count = 0
	while True:
		try:
			driver.find_element_by_id('pagelet_timeline_medley_photos')
			break
		except:
			pass

		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		scroll_count += 1
		print('Scrolling Down #' + str(scroll_count) + '...')
		sleep(random() * 1.3 + 1.2)

	html = driver.page_source
	soup = BeautifulSoup(html, 'html.parser')
	friend_lis = soup.find_all('li', class_ = '_698')
	friend_as = [friend_li.div.a['href'] for friend_li in friend_lis]

	data = {}
	data['friend_urls'] = []
	data['friends'] = []
	for friend_li in friend_lis:
		data['friend_urls'].append({
			'url': friend_li.div.a['href']
		})

	# writing to JSON output file
	with open('data.json', 'w') as outfile:
		print('Data Length:', len(data['friend_urls']))
		json.dump(data, outfile)
else:
	# read data from JSON file (for debugging or rebooting scraper)
	last_data_file = 'data.json'
	with open(last_data_file) as json_file:
		data = json.load(json_file)

# method to scrape section for data under friend's profile
def scrape_friend_section(friend, friend_prop, div_id, children_classes):
	sleep(random() * 1.6 + random() * 2.2 + 2.5)
	html = driver.page_source
	soup = BeautifulSoup(html, 'html.parser')
	section_divs = soup.find('div', {'id': div_id}).findChildren('div', {'class': children_classes})
	friend[friend_prop] = []
	for section_div in section_divs:
		try:
			val = ''
			if friend_prop == 'education':
				val = section_div.a.text
			elif friend_prop == 'residences':
				if len(section_div.div.text) > 0:
					val = section_div.span.a.text + '#' + section_div.div.text
			elif friend_prop == 'contact':
				val = section_div.div.div.span.ul.li.span.text
			elif friend_prop == 'basic':
				val = section_div.div.div.span.text

			if val != '':
				friend[friend_prop].append(val)
		except:
			pass

	sleep(random() * 2.3 + 3.3)

# iterate through friends and scrape profile sections for data
friend_count = len(data['friends'])
for i in range(friend_count, len(data['friend_urls'])):
	friend_url = data['friend_urls'][i]
	driver.get(friend_url['url'])
	friend_raw = {
		'name': driver.find_element_by_css_selector('a._2nlw').text
	}

	# scrape raw data
	about_button = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "//a[@class='_6-6'][@data-tab-key='about']")))
	about_button.click()
	friend_count += 1	
	print('Scraping Friend #' + str(friend_count) + '...')

	education_button = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "//a[@data-testid='nav_edu_work']")))
	education_button.click()
	print('Scraping Education...')
	scrape_friend_section(friend_raw, 'education', 'pagelet_eduwork', ['_2lzr', '_50f5', '_50f7'])

	places_button = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "//a[@data-testid='nav_places']")))
	places_button.click()
	print('Scraping Residences...')
	scrape_friend_section(friend_raw, 'residences', 'pagelet_hometown', ['_6a', '_6b'])

	contact_button = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "//a[@data-testid='nav_contact_basic']")))
	contact_button.click()
	print('Scraping Contact Information...')
	scrape_friend_section(friend_raw, 'contact', 'pagelet_contact', ['_4bl7', '_pt5'])
	scrape_friend_section(friend_raw, 'basic', 'pagelet_basic', ['_4bl7', '_pt5'])

	# reprocess data to fit into new friend object
	friend = {
		'name': friend_raw['name'],
		'education': friend_raw['education'],
		'current_city': None,
		'hometown': None,
		'phone': None,
		'email': None,
		'birthday': None,
		'gender': None
	}

	for city in friend_raw['residences']:
		if 'Hometown' in city:
			friend['hometown'] = city.split('#')[0]
		else:
			friend['current_city'] = city.split('#')[0]

	for contact in friend_raw['contact']:
		if '(' in contact and len(contact) == 14 and int(contact[-2:]) > 0:
			friend['phone'] = contact
		elif '@' in contact:
			friend['email'] = contact

	for basic_info in friend_raw['basic']:
		if 'January' in basic_info or 'February' in basic_info or 'March' in basic_info or 'April' in basic_info or \
			'May' in basic_info or 'June' in basic_info or 'July' in basic_info or 'August' in basic_info or \
			'September' in basic_info or 'October' in basic_info or 'November' in basic_info or 'December' in basic_info:
			friend['birthday'] = basic_info.split(',')[0]
		elif 'Male' in basic_info or 'Female' in basic_info or 'Other' in basic_info:
			friend['gender'] = basic_info

	data['friends'].append(friend)
	print(friend)

	with open('data.json', 'w') as outfile:
		print('Data Length:', len(data['friend_urls']))
		json.dump(data, outfile)

	sleep(random() * 2.1 + 1.3)

# reprocess data to represent unique places
print('Reprocessing Data for Places...')
data['friend_places'] = {
	'schools': {},
	'current_cities': {},
	'hometowns': {}
}

for friend in data['friends']:
	for school in friend['education']:
		data['friend_places']['schools'].setdefault(school, []).append(friend['name'])

	data['friend_places']['current_cities'].setdefault(friend['current_city'], []).append(friend['name'])
	data['friend_places']['hometowns'].setdefault(friend['hometown'], []).append(friend['name'])

with open('data.json', 'w') as outfile:
	print('Data Length:', len(data['friend_urls']))
	json.dump(data, outfile)

print('End of Program...')