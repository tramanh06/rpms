import os
import glob
import utils
import logging
import utils

def is_paper_seen(papers_index, paper):
    return paper in papers_index


def get_path_leave(path):
    head, tail = os.path.split(path)
    return tail or os.path.basename(head)


papers_DIR = os.path.join(os.path.dirname(__file__), "papers/")
dataset_DIR = os.path.join(os.path.dirname(__file__), "dataset/")

utils.is_folder_exists_create_otherwise(dataset_DIR)

index = 0
papers_collection = []
author_papers_dict = {}

for author_dir in glob.glob(papers_DIR + '*' + os.path.sep):
    author = get_path_leave(author_dir)
    papers_id = []
    print 'author= ' + author

    for paper_filename in glob.glob(author_dir + '*.pdf'):
        paper_title = os.path.basename(paper_filename).replace(".pdf", "")
        if not is_paper_seen(papers_collection, paper_title):
            papers_collection.append(paper_title)

            pdfPath = paper_filename
            print "pdfPath = " + pdfPath
            fileNameOut = dataset_DIR + "p" + str(index) + ".txt"
            logging.info('converting (%s %s -> %s)' % ("pdftotext", pdfPath, fileNameOut))
            os.system(""" %s "%s" "%s" """ % ("pdftotext", pdfPath, fileNameOut))
            papers_id.append(index)
            index += 1
        else:
            paper_id = papers_collection.index(paper_title)
            papers_id.append(paper_id)
            print "***** Paper " + paper_title + " already exists. Paperid=" + str(paper_id)
        
    author_papers_dict[author] = papers_id

utils.write_to_json_file("dataset/authors.json", author_papers_dict)


        