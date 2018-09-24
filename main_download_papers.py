import utils
from paper_crawling import arxiv_crawler, dblp_crawler
import logging
from logging.config import fileConfig
import configparser
import os
import collections
import pickle
import googleapiclient
import argparse

fileConfig('logging_config.ini')
logger = logging.getLogger()

config = configparser.ConfigParser()
config.read('venv/keys.ini')
my_api_key = config['GOOGLE']['API_KEY']
my_cse_id = config['GOOGLE']['CSE_ID']


def download_papers(researcher):
    # Look up researcher from dblp to get list of publications
    author_results = dblp_crawler.dblp_crawler(researcher)
    dblp_crawler.print_publication_list(author_results)

    papers_DIR = os.path.join("papers", researcher.replace(" ", "_"), "")  # Only works when python file is run in the project root location

    # Download papers from arxiv, store in papers_DIR="papers/AUTHOR_NAME"
    for author, publications in author_results.items():
        papers = [pub['title'] for pub in publications]

        utils.is_folder_exists_create_otherwise(papers_DIR)

        logging.info("Downloading paper...")
        arxiv_crawler.download_list_of_papers_serial(
            titles=papers,
            dirname=papers_DIR,
            my_api_key=my_api_key,
            my_cse_id=my_cse_id)

        logging.info("Downloaded %s out of %s papers", get_files_count(papers_DIR), len(papers))


def get_files_count(DIR): 
    return len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])


def get_papers(author_results):
    papers_list_of_list = author_results.values()
    publications = utils.flatten(papers_list_of_list)
    titles = [x['title'] for x in publications]
    return titles


def load_papers_title(researchers):
    researcher_papers = collections.OrderedDict([(researcher, get_papers(dblp_crawler.dblp_crawler(researcher))) for researcher in researchers])
    return researcher_papers


def auto_download(researcher_papers_location=None, researchers_file_location=None):
    # researcher_papers_location = "researchers_to_papers.p"

    if os.path.isfile(researcher_papers_location):
        researcher_papers = pickle.load( open( researcher_papers_location, 'rb'))
    else:
        researchers = utils.read_file(file_location=researchers_file_location, sep="|").split("|")
        researchers = [name.title() for name in researchers]  # Convert "David HSU" to "David Hsu"
        researcher_papers = load_papers_title(researchers)

    for researcher, papers in researcher_papers.items():
        papers_DIR = os.path.join("papers", researcher.replace(" ", "_"), "")
        utils.is_folder_exists_create_otherwise(papers_DIR)

        try:
            arxiv_crawler.download_list_of_papers_serial(
                titles=papers,
                dirname=papers_DIR,
                my_api_key=my_api_key,
                my_cse_id=my_cse_id)
            del researcher_papers[researcher]
        except Exception as e:
            completed_up_to = int(utils.read_file("index_marker.txt"))
            researcher_papers[researcher] = researcher_papers[researcher][completed_up_to:]
            pickle.dump( researcher_papers, open( researcher_papers_location, "wb" ) )
            utils.write_to_file("researchers1.txt", "\n".join(researcher_papers.keys()))
            logging.error(str(e))
            break



def main():
    # researchers = ["Leong Tze Yun", "Bryan Low", "Harold Soh", "David Hsu", "Kuldeep S. Meel", "Lee Wee Sun"]
    # researchers = ["Shang-Wei LIN", "Adams Wai-Kin KONG", "Wee Keong NG", "Anupam CHATTOPADHYAY"]
    # researchers = utils.read_file(file_location="researchers.txt", sep="|").split("|")
    # researchers = [name.title() for name in researchers]  # Convert "David HSU" to "David Hsu"

    # for researcher in researchers:
    #     download_papers(researcher)
    auto_download()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Downloading papers')

    parser.add_argument('-p', '--pickled', help='Location of pickled file that includes researchers name and their papers', required=False)
    parser.add_argument('-r', '--researchers', help='Location of list of researchers', required=False)
    args = vars(parser.parse_args())

    '''researcher_papers_location="researchers_to_papers.p"'''
    '''researchers_file_location="researchers.txt"'''
    auto_download(args['pickled'], args['researchers'])
