import unittest
import logging
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paper_crawling import arxiv_crawler
from timeit import default_timer as timer


class MyTestCase(unittest.TestCase):
    def setUp(self):
        logging.getLogger().setLevel(logging.INFO)
        

    def test_single_download(self):
        start = timer()
        title = '"Gaussian Process Decentralized Data Fusion Meets Transfer Learning in Large Scale Distributed Cooperative Perception"'  # title must be exact
        arxiv_crawler.download_from_arxiv(title)
        end = timer()
        print "Time taken for single: "
        print end - start

    def test_list_download_parallel(self):
        start = timer()
        titles = ['"Gaussian Process Decentralized Data Fusion Meets Transfer Learning in Large Scale Distributed Cooperative Perception"',
                  '"Causal Mechanism-based Model Construction."']
        arxiv_crawler.download_list_of_papers_parallel(titles)
        end = timer()
        print "Time taken for parallel: "
        print end - start

    @unittest.skip("Skip")
    def test_list_download_serial(self):
        start = timer()
        titles = ['"Gaussian Process Decentralized Data Fusion Meets Transfer Learning in Large Scale Distributed Cooperative Perception"',
                  '"Causal Mechanism-based Model Construction."']
        arxiv_crawler.download_list_of_papers_serial(titles)
        end = timer()
        print "Time taken for serial: "
        print end - start

if __name__ == '__main__':
    unittest.main()