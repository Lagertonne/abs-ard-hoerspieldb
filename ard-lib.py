import requests
import pprint
from bs4 import BeautifulSoup
from lxml import etree

def search_book(query, author="", page=0):
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
		"tx_drahsdbsearch_hsdbsearch[search][seite]": str(page),
	}

	search_url = "https://hoerspiele.dra.de/suche/"

	# Make initial request
	search_results = requests.post(search_url, data=search_params)

	if search_results.status_code == 200:
		soup = BeautifulSoup(search_results.content, "html.parser")

	results = soup.find('table', class_='resultTable').find('tbody').find_all('tr')

	# We waste one request to get the page count
	page_count = len(soup.find('div', class_='pager').get_text().strip().splitlines())

	audiobook_results = []

	for page_num in range(0, page_count):
		page = page_num
		search_url = "https://hoerspiele.dra.de/suche/"

		# Make initial request
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
			book["production"] = parsed_row[2].get_text()
			book["date"] = parsed_row[3].get_text()
			book["type"] = parsed_row[4].find('img').get('title')
			audiobook_results.append(book)

	page_count = len(soup.find('div', class_='pager').get_text().strip().splitlines())
	print(page_count)


	return audiobook_results


result_books = search_book(query="Steppenwolf")
pprint.pprint(result_books)
print(len(result_books))

