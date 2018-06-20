'''
This package calls the dblp REST api to retrieve structured list of
publications given an author name
'''


import dblp
import requests
import json

def query_dblp_by_author(author):
    author = author.replace(' ', '_')
    url_template = "http://dblp.org/search/publ/api?q=author%3A<AUTHOR_NAME>%3A&format=json"
    response = requests.get(url_template.replace("<AUTHOR_NAME>", author))
    return response


author_name = 'Bryan Low'
authors = dblp.search(author_name)
print 'Found ' + str(len(authors)) + ' authors:'
print ', '.join(map(lambda x: str(x), authors))

print 'List of publications:'
for author in authors:
    print str(author) + ':'
    response = query_dblp_by_author(str(author))
    if response.ok:
        # print response.json()
        parsed_json = response.json()
        print parsed_json['result']['hits']['hit'][0]['info']['title']

