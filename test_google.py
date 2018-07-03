from googleapiclient.discovery import build
import pprint
import urllib
import os
import configparser

config = configparser.ConfigParser()
config.read('venv/keys.ini')

my_api_key = config['GOOGLE']['API_KEY']
my_cse_id = config['GOOGLE']['CSE_ID']


def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']

results = google_search(
    '"SEAPoT RL   Selective Exploration Algorithm for Policy Transfer in RL"' + ' filetype:PDF', 
    my_api_key, my_cse_id, num=10)

downloaded_pdf = "abc.pdf"
for result in results:
    pdf_url = result['link']
    print pdf_url
    urllib.urlretrieve(pdf_url, downloaded_pdf)
    if os.path.getsize(downloaded_pdf) > 10000:
        break


# for result in results:
#     pprint.pprint(result)
