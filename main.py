'''
Author: TramAnh Nguyen 
File Created: Monday, 25th June 2018 9:22:16 am
-----
Last Modified: Monday, 25th June 2018 10:07:50 am
Modified By: TramAnh Nguyen 
-----
'''
from paper_crawling import dblp_crawler, arxiv_crawler
import os
import logging
from logging.config import fileConfig

fileConfig('logging_config.ini')
logger = logging.getLogger()

researcher = "Bryan Low"

author_results = dblp_crawler.dblp_crawler(researcher)
dblp_crawler.print_publication_list(author_results)

for author, publications in author_results.items():
    papers = [pub['title'] for pub in publications]

    outDIR = "papers/"
    # Check if output folder has been created. Create otherwise
    try:
        os.makedirs(outDIR)
    except OSError:
        if not os.path.isdir(outDIR):
            raise

    logging.info("Downloading paper...")
    arxiv_crawler.download_list_of_papers(papers[0:5], dirname=outDIR)


