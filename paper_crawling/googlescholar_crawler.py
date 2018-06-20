import scholarly

' Query abstracts of last 2 years '
author_name = 'Bryan Low'
search_query = scholarly.search_author(author_name)
print "Author's summary:"
author_string = next(search_query)
print author_string

author = author_string.fill()

print "Print the titles of the author's publications"
print [pub.bib['title'] for pub in author.publications]

# Take a closer look at the first publication
print "Print abstract of the first publication"
pub = author.publications[0].fill()
print pub

# author = next(search_query).fill()