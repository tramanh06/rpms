import utils
from paper_crawling import arxiv_crawler, dblp_crawler
import logging
from logging.config import fileConfig
import configparser


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

    papers_DIR = "papers/" + researcher.replace(" ", "_") + "/"  # Only works when python file is run in the project root location

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


def main():
    researchers = ["Leong Tze Yun", "Bryan Low", "Harold Soh", "David Hsu", "Kuldeep S. Meel", "Lee Wee Sun"]

    for research in researchers:
        download_papers(research)


if __name__ == '__main__':
    main()
