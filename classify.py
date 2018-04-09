# import libraries
import urllib2
from bs4 import BeautifulSoup
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
from pprint import pprint
import numpy as np
import pickle

# specify the url
quote_page = "http://www.crunchyroll.com/comics/manga"

# query the website and return the html to the variable 'page'
page = urllib2.urlopen(quote_page)

# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(page, 'html.parser')

# Take out the <div> of name and get its value
images = soup.find_all('img')

#for image in images	:
	#print image['src']

# open text file
with open('token.txt', 'r') as myfile:
    key = myfile.read().replace('\n', '')
# initialize clarifai
app = ClarifaiApp(api_key=key)

# use clarafai
model = app.models.get('general-v1.3')


sex = ["male", "man", "men", "boy", "woman", "women", "female", "girl"]
sexes = [] # where 0 is a male and 1 is a female

for i in np.arange(len(images)):
	image = ClImage(url=images[i]['src'])

	# edge cases
	if(images[i]['src'] == "http://img1.ak.crunchyroll.com/i/croll_manga/59242caf905ce4442bdf926171522d18_1408942446_large.jpg" 
		or not images[i]['src'].startswith("http") or not ("jpg" in images[i]['src'])):
		continue;

	# gets just the classifications in order of highest proability 
	output = model.predict([image])
	output = output['outputs'][0]['data']['concepts']

	for classification in output: # goes through classifications of one image
		if classification['name'] in sex:
			# find which sex it is equal to
			boolarr = [1 if classification['name'] == i else 0 for i in sex]  # (0 0 0 1 0 0 0)
			print(classification['name'])
			# find which string it's equal to 
			one = boolarr.index(1)
			if (one in np.arange(0,4)):
				sexes.append(0) 
			else:
				sexes.append(1)
			break;
	if i == 100:
		break;

print(sexes)
print(np.count_nonzero(sexes)/len(sexes), "% of manga feature a woman")