import requests
import pprint
from bs4 import BeautifulSoup
from lxml import etree

def get_single_book(id):
	url = "https://hoerspiele.dra.de/detailansicht/"

	book_page = requests.get(url + str(id))

	if book_page.status_code == 200:
		soup = BeautifulSoup(book_page.content, "html.parser")

	book = {}

	book["title"] = soup.find('h1', class_="ti").get_text()
	book["author"] = soup.find_all('a', {'data-id': 'autor'})[0].get_text()
	book["description"] = soup.find_all('p', class_="cuttext")[0].get_text()
	book["cover"] = "https://hoerspiele.dra.de/" + soup.find('div', class_="column is-one-third").find('figure', class_="image").find('img')['src']

	book["publisher"] = soup.find("strong", string="Produktions- und Sendedaten").parent.parent.find_all('li')[0].get_text()

	date_string = soup.find("strong", string="Produktions- und Sendedaten").parent.parent.find_all('li')[1].get_text()

	book["publishedYear"] = date_string.split("|")[0].split(":")[1].strip().split(".")[-1]

	book["type"] = ""

	try:
		series = {}
		series["series"] = soup.find('strong', string="Reihentitel:").parent.find('a', {'data-id': 'titel'}).get_text()
		book["series"] = [series]
	except AttributeError:
		pass

	return book


def search_book(query, author=""):
	page = 0

	search_params = {
		"tx_drahsdbsearch_hsdbsearch[__referrer][@extension]": "DraHsdbsearch",
		"tx_drahsdbsearch_hsdbsearch[__referrer][@controller]": "Search",
		"tx_drahsdbsearch_hsdbsearch[__referrer][@action]": "search",
		"tx_drahsdbsearch_hsdbsearch[__referrer][arguments]": "YTowOnt9cd119c62bc86ce05d569a006db4286ede1e5921d",
		"tx_drahsdbsearch_hsdbsearch[__referrer][@request]": "{\"@extension\":\"DraHsdbsearch\",\"@controller\":\"Search\",\"@action\":\"search\"}1d294c1daabcc5557450341c6e27478b9df8a433",
		"tx_drahsdbsearch_hsdbsearch[__trustedProperties]": "{\"search\":{\"bestand\":1,\"ueberall\":1,\"titel\":1,\"autor\":1,\"regie\":1,\"sprecher\":1,\"mitwirkende\":1,\"gattung\":1,\"gattungop\":1,\"gattungmulti\":1,\"produzent\":1,\"preise\":1,\"pjahr\":1,\"erstsendungvon\":1,\"erstsendungbis\":1,\"dauervon\":1,\"dauerbis\":1,\"bnr\":1,\"ttv\":1,\"erweitert\":1,\"hoerbar\":1,\"pager\":1,\"mehrteilertitel\":1,\"sort\":1,\"sortkey\":1,\"seite\":1,\"showhits\":1}}9e4ad30c60f8d96ac881218e44ea65875f55b11d",
		"tx_drahsdbsearch_hsdbsearch[search][sort]": "",
		"tx_drahsdbsearch_hsdbsearch[search][sortkey]": "",
		"tx_drahsdbsearch_hsdbsearch[search][showhits]": "10",
		"tx_drahsdbsearch_hsdbsearch[search][erweitert]": "1",
		"tx_drahsdbsearch_hsdbsearch[search][ueberall]": query,
		"tx_drahsdbsearch_hsdbsearch[search][hoerbar]": [
			"0",
			""
		],
		"tx_drahsdbsearch_hsdbsearch[search][bestand]": "alle",
		"tx_drahsdbsearch_hsdbsearch[search][titel]": "",
		"tx_drahsdbsearch_hsdbsearch[search][mehrteilertitel]": "",
		"tx_drahsdbsearch_hsdbsearch[search][autor]": author,
		"tx_drahsdbsearch_hsdbsearch[search][regie]": "",
		"tx_drahsdbsearch_hsdbsearch[search][sprecher]": "",
		"tx_drahsdbsearch_hsdbsearch[search][mitwirkende]": "",
		"tx_drahsdbsearch_hsdbsearch[search][gattungmulti]": "",
		"tx_drahsdbsearch_hsdbsearch[search][gattungop]": [
			"or",
			"or"
		],
		"tx_drahsdbsearch_hsdbsearch[search][gattung]": "alle",
		"tx_drahsdbsearch_hsdbsearch[search][produzent]": "alle",
		"tx_drahsdbsearch_hsdbsearch[search][preise]": "alle",
		"tx_drahsdbsearch_hsdbsearch[search][pjahr]": "",
		"tx_drahsdbsearch_hsdbsearch[search][erstsendungvon]": "",
		"tx_drahsdbsearch_hsdbsearch[search][erstsendungbis]": "",
		"tx_drahsdbsearch_hsdbsearch[search][dauervon]": "",
		"tx_drahsdbsearch_hsdbsearch[search][dauerbis]": "",
		"tx_drahsdbsearch_hsdbsearch[search][bnr]": "",
		# "tx_drahsdbsearch_hsdbsearch[search][ttv]": "",
		# "tx_drahsdbsearch_hsdbsearch[search][erweitert]": "",
		# "tx_drahsdbsearch_hsdbsearch[search][hoerbar]": "",
		# "tx_drahsdbsearch_hsdbsearch[search][pager]": "Nc27CoAwDIXhd8ncwZhYa1dHR59AJF5AFGwdRHx3o9jxO3D4L9glHEts5AzgL8AMPFeuQioMICaQIv+ROwV9sI4yBYNHJlvy+ykSWGET6DZ/qd6ONepcGgjS7f3USozzOmp+6JYg9wM=",
		# "tx_drahsdbsearch_hsdbsearch[search][mehrteilertitel]": "",
		# "tx_drahsdbsearch_hsdbsearch[search][sort]": "",
		# "tx_drahsdbsearch_hsdbsearch[search][sortkey]": "dat",
		"tx_drahsdbsearch_hsdbsearch[search][seite]": "0",
	}

	search_url = "https://hoerspiele.dra.de/suche/"

	# Make initial request
	search_results = requests.post(search_url, data=search_params)

	if search_results.status_code == 200:
		soup = BeautifulSoup(search_results.content, "html.parser")

	results = soup.find('table', class_='resultTable').find('tbody').find_all('tr')

	# We waste one request to get the page count
	page_count = len(soup.find('div', class_='pager').get_text().strip().splitlines())

	audiobook_search_results = []

	for page_num in range(0, page_count):
		print("page ", page_num)

		search_url = "https://hoerspiele.dra.de/suche/"

		# Make initial request
		search_params["tx_drahsdbsearch_hsdbsearch[search][seite]"] = str(page_num)
		search_results = requests.post(search_url, data=search_params)

		if search_results.status_code == 200:
			soup = BeautifulSoup(search_results.content, "html.parser")

		results = soup.find('table', class_='resultTable').find('tbody').find_all('tr')

		for row in results:
			book = {}
			parsed_row = row.find_all('td')
			# Titel, Autor, Produktion, Datum, Gattung
			book["title"] = parsed_row[0].get_text()
			book["author"] = parsed_row[1].get_text()
			book["detail"] = parsed_row[0].find('a').get('href').split('/')[-1]
			audiobook_search_results.append(book)

	page_count = len(soup.find('div', class_='pager').get_text().strip().splitlines())

	# Get details for all books
	audiobooks_detail = []
	for book in audiobook_search_results:
		audiobooks_detail.append(get_single_book(book["detail"]))

	return audiobooks_detail

if __name__ == '__main__':
	#get_single_book(1428095)
	#get_single_book(5036211)
	pprint.pprint(len(search_book(query="Steppenwolf")))