'''
This package calls the dblp REST api to retrieve structured list of
publications given an author name
'''
# import requests
# import json


# def get_from_dblp(url):
#     print 'Querying request from ' + url
#     r = requests.get(url)
#     return r


# def urlify(str):
#     return str.replace(' ', '+')


# def get_conferences():

# author_name = "Bryan Low"
# url_format = "http://dblp.org/search/publ/api?q=<AUTHOR_NAME>&h=1000&format=json"
# url = url_format.replace("<AUTHOR_NAME>", urlify(author_name))
# response = get_from_dblp(url)
# print response.json()


import dblp
authors = dblp.search('bryan low')
print authors[1].publications[0].journal
