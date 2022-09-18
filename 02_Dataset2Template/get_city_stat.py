
import json
from textwrap import indent
from bs4 import BeautifulSoup
import requests

S = requests.Session()

URL = "https://ko.wikipedia.org/w/api.php"

SEARCHPAGE = "서울특별시"

PARAMS = {
    "action": "parse",
    "format": "json",
    "page": SEARCHPAGE
}

R = S.get(url=URL, params=PARAMS)
DATA = R.json()
DATA["parse"]["text"]["*"]
to_html = BeautifulSoup(DATA["parse"]["text"]["*"],'lxml')
area_head = to_html.find("a",{"title":"넓이"}) #start from infobox
print(area_head.find_next("td").text)
print(type(to_html))


