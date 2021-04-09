from bs4 import BeautifulSoup
import requests
import sys

def GetInfo(fwlink=None, imdblink=None, odp=None):
	result = [] #[imdbRating, fwRating, category, year, description]
	if imdblink:
		resp = requests.get(imdblink, timeout=5)
		odp = BeautifulSoup(resp.content, "html.parser")
		temp = odp.find_all("span", {"itemprop": "ratingValue"})
		try:
			result.append(temp[0].string.extract())
		except Exception:
			result.append('')
	if fwlink:
		resp = requests.get(fwlink, timeout=5)
		odp = BeautifulSoup(resp.content, "html.parser", from_encoding="utf=8")
		if odp.find('filmRating__rateValue'):
			attrs = [["span", {"class": "filmRating__rateValue"}]]
		else:
			attrs = [["span", {"itemprop": "ratingValue"}]]
		attrs.extend([["div", {"itemprop": "genre"}],
					["span", {"class": "filmCoverSection__year"}], ["span", {"itemprop": "description"}]])
		for i in attrs:
			temp = odp.find(i[0], i[1])
			try:
				toAdd = []
				for x in temp.stripped_strings:
					toAdd.append(x)
				if len(toAdd)==1:
					result.extend(toAdd)
				else:
					result.append(toAdd)
			except AttributeError:
				print("AttributeError --> %s" % i)
				result.append('')
		result[-1].replace('\xa0', ' ')
	return result	
