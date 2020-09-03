from requests import get
from bs4 import BeautifulSoup
import re

# Base path
citedByPath = 'https://www.ncbi.nlm.nih.gov/pmc/articles/{}/citedby/'
# Headers for requests
headers = {
    'authority': 'www.ncbi.nlm.nih.gov',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-US,en;q=0.9,tr;q=0.8',
}

#Fetch cited articles
resp = get(citedByPath.format("PMC7181908"), headers=headers).text

#Init beautifulsoup
soup = BeautifulSoup(resp, 'lxml')

#Get cited count
found_cited = soup.select_one('#maincontent > div.hide-overflow.toc.page-box-wide > form > h2').get_text()
found_cited = re.findall('\\d+', found_cited)[0]

#Grab list
cited_list = soup.find_all('div', class_='rprt')

cited_ids = []
for cited_item in cited_list:
    pmc_section = cited_item.find('dl', class_='rprtid')
    cited = pmc_section.find('dd').get_text().strip()
    cited_ids.append(cited)

print('Found', found_cited, 'articles')
print('#' * 20)
print(cited_ids)