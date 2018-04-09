# import libraries
import urllib2
from bs4 import BeautifulSoup

# specify the url
quote_page = "http://www.crunchyroll.com/comics/manga"

# query the website and return the html to the variable 'page'
page = urllib2.urlopen(quote_page)

# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(page, 'html.parser')

# Take out the <div> of name and get its value
images = soup.find_all('img')

for image in images	:
	print image['src']