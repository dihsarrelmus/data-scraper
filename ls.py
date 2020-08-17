from selenium import webdriver #Allows launch/initialise browser
from selenium.webdriver.common.by import By #Allows search for things using specific parameters
from selenium.webdriver.support.ui import WebDriverWait # Allows to wait for page to load
from selenium.webdriver.support import expected_conditions as EC #Specify what the saerch is
from bs4 import BeautifulSoup as bs
import csv
import time

option_or = input('Search for an individual or search for an organization? Enter I if looking for individual or enter O if looking for organization: ' )
if option_or == 'I' or option_or == 'i':
	nome_ = input('Enter Last Name:')
	answer = input('Would you like to enter a first name ? Answer with a Y or N: ' )

	if answer == 'Y' or answer == 'y':
		nome_2 = input('Enter first name')
	elif answer == 'N' or answer == 'n':
		pass
elif option_or == "O" or option_or == "o":
	organization = input('Enter Organization Name: ')

file_name = input('What will you name this file ?')
add_extension = file_name + '.csv'

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
driver = webdriver.Chrome(chrome_options=options)

driver.get('https://ouf.osc.state.ny.us/ouf/')

last_name = driver.find_element_by_id('lastName')
first_name = driver.find_element_by_id('firstName')
organization_name = driver.find_element_by_id('companyName')

if option_or == 'I' or option_or == 'i':
	last_name.send_keys(nome_)
	if answer == 'Y' or answer == 'y':
		first_name.send_keys(nome_2)
elif option_or == 'O' or option_or == 'o':
	organization_name.send_keys(organization)

if option_or == 'I' or option_or == 'i':
	nextButton = driver.find_element_by_css_selector('.btn.btn-custom').click()
elif option_or == 'O' or option_or == 'o':
	organizationsearch = driver.find_element_by_name('searchCompany').click()

names_list = []
addresses_list =[]
reported_by = []
type_of_property = []
ouf_code = []
year_reported = []

def get_current():
	links = [link.get_attribute('href') for link in driver.find_elements_by_xpath('//*[@title="Display Claim Details"]')[::2] ]
	time.sleep(5)
	grab = driver.page_source # Downloads web page 
	soup = bs(grab, 'html.parser')
	da_ta = soup.find('tbody').find_all('tr')
	for each in da_ta[0:]:
		try:  
			names = each.find('a', class_=False, id=False).find_next('span').get_text()
			names = names.title()
			names_list.append(''.join(names.split(',')))
			addresses = each.find('span').find_next('span').get_text()
			addresses = addresses.title()
			addresses_list.append(''.join(addresses.split(',')))
			reports = each.find('div', text=True).get_text()
			reports = reports.title()
			reported_by.append(''.join(reports.split(','))) 
		except:
			pass
	for link in links:
		driver.get(link)
		find_file = driver.page_source
		beauty = bs(find_file, 'html.parser')
		top = beauty.find_all('li' ,class_='list-group-item-text')
		top5 = top[5].get_text()
		top5 = top5.title()
		type_of_property.append(top5)
		ouf = beauty.find('label', id ='oufCode').find_next('span').get_text()
		ouf_code.append(ouf)
		yr = beauty.find('label',id='yearReported').find_next('span').get_text()
		year_reported.append(yr)
def go_on():
	driver.find_element_by_name('buttons:cancel').click()
def diende():
	driver.find_element_by_link_text('>')


go_to = []
'''get_current()
go_on()'''
try:
	diende()
except Exception as e :
	print ("This exception sucks" + str(e))
	get_current()
	with open(add_extension,'w',newline='') as f: # creates new file and makes write to file command 
		writer = csv.writer(f) 
		writer.writerows(zip(names_list,addresses_list,reported_by,type_of_property,ouf_code,year_reported))
	time.sleep(15)
	driver.quit()

elements = driver.find_element_by_class_name('navigator').find_element_by_tag_name('span').text
for i in elements:
	if i == ' ' or i == '<' or i == ' ' or i == '>'  : #double parenthesis space
		pass
	else:
		go_to.append(int(i))

for each_num in go_to[:-1]:
	get_current()
	go_on()
	time.sleep(13)
	now = driver.find_element_by_link_text('>').click()
get_current()
		
with open(add_extension,'w',newline='') as f: # creates new file and makes write to file command 
	writer = csv.writer(f) 
	writer.writerows(zip(names_list,addresses_list,reported_by,type_of_property,ouf_code,year_reported))

driver.quit()
   	
        
