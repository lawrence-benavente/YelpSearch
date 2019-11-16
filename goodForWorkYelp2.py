#! python3
# goodForWorkYelp.py - Scan all of multiple yelp pages to see if it follows certain attributes and conditions
#input: the type of shop (ex: coffee, tea, etc.), location
#output: how many of those shops follow attributes (ex: good for work)

import requests, bs4, sys
from selenium import webdriver

#Retreive shop-type and location from command line
shopType = sys.argv[1]
location = sys.argv[2]

#Open yelp search for specific shop-type and location and by top rated
yelpGen = requests.get('http://yelp.com//search?find_desc=' + shopType + '&find_loc=' + str(location) +'&sortby=rating')
yelpGen.raise_for_status()
genSoup = bs4.BeautifulSoup(yelpGen.text, "html.parser")

#Store url of restaraunts in array
restraunts = []
for aTab in genSoup.find_all("a", "lemon--a__373c0__IEZFH link__373c0__29943 link-color--blue-dark__373c0__1mhJo link-size--inherit__373c0__2JXk5"):
	if '?osq' in str(aTab.get('href')):
		restraunts.append(aTab.get('href'))

goodRestraunts = []
goodRestrauntsURL = []
#Open individual restraunt Yelp page
for i in range(len(restraunts)):
	try: 			# Insert try incase of keyboard interruption
		#Set Up Selenium
		browser = webdriver.Chrome()
		browser.get('http://yelp.com' + restraunts[i])

		#Locate more attributes button and click
		try:			#Insert try in case there is no button to press
			buttonAll = browser.find_element_by_partial_link_text('More Attributes')
			buttonAll.click()
		except:
			pass

		# Pass Selenium script to Beautiful Soup
		page_source = browser.page_source
		browser.close()
		resSoup = bs4.BeautifulSoup(page_source, 'html.parser')

		#Sparse through page to check if it is Attributes and Condition
		attribute = 'Good for Working'
		condition = 'Yes'
		for spanTab in resSoup.find_all("div", "lemon--div__373c0__1mboc arrange-unit__373c0__1piwO arrange-unit-fill__373c0__17z0h border-color--default__373c0__2oFDT"):
			if '20' in str(spanTab): 					#Make sure not a review
				pass
			else:
				if attribute in str(spanTab):		#Choosing Attributes
					if condition in str(spanTab):			#Choosing Condition
						goodRestrauntsURL.append(restraunts[i])
						goodRestraunts.append(resSoup.h1.string)	#Save Restraunt Name
						break
	except:
		print('There was a keyboard interruption or the window was closed prematurely.')
		break

#Print Results
print('There are ' + str(len(goodRestraunts)) + ' results out of ' + str(i) + ' searches that match:')
print(*goodRestraunts, sep = "\n")