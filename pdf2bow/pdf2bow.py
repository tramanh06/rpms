import argparse
import codecs
from glob import glob
import os
import re
import sys

from sanitize import sanitize
from ispdf import ispdf
import bow
import utils
import configparser
import logging

sys.path += ['.']
parentDirectory = os.path.dirname(__file__)

#####################################################################
# PURPOSE:
#  - encodes all pdfs in a directory as Bag of Words
#
# PRE-REQUISITES:
# - requires a pdf2txt utility to be available (pdf2textCMD variable)
# - the script can also stem if given access to a stemmer (stemmerCMD variable)
#
# Author: Laurent Charlin (lcharlin@cs.toronto.edu)
# Modified by: Tram Anh Nguyen (tramanh06@gmail.com)
#
#####################################################################

pdf2textCMD = "pdftotext"


def pdf_bow(pdfPath, outDIR, pdfFile=None, overwrite=False):
    """Convert a pdf file to stemmed, tokenized, non-stopword strings.

    Args:
        pdfPath (str): Path to pdf
        outDIR (str): Directory where the bag-of-word file will be stored
        
    Returns:
        Filename of the bow file. Bag-of-word file will be created in the outDIR folder

    """

    logging.info('- %s:' % pdfPath)

    # Check if out folder exists, create otherwise
    utils.is_folder_exists_create_otherwise(outDIR)

    if pdfFile is None:
        if not os.path.isdir(outDIR):
            try:
                os.mkdir(outDIR)
            except OSError, e:
                logging.error('Problem creating directory...')
                raise
        pdfFile = os.path.basename(pdfPath)
        if re.search('\.[a-zA-Z0-9]{1,4}', pdfFile):
            fileNameOut = outDIR + re.sub('\.[a-zA-Z0-9]{1,4}$', '.txt', pdfFile)
            fileNameOutBow = outDIR + \
                re.sub('\.[a-zA-Z1-9]{1,4}$', '.bow', pdfFile)
        else:
            fileNameOut = outDIR + pdfFile + '.txt'
            fileNameOutBow = outDIR + pdfFile + '.bow'
    else:
        fileNameOut = outDIR + pdfFile + '.txt'
        fileNameOutBow = outDIR + pdfFile + '.bow'

    # get text
    if not os.path.isfile(fileNameOut) or os.path.getsize(fileNameOut) == 0 or overwrite:
        logging.info('converting (%s %s -> %s)' % (pdf2textCMD, pdfPath, fileNameOut))
        os.system(""" %s "%s" "%s" """ % (pdf2textCMD, pdfPath, fileNameOut))
    else:
        logging.info('not converting since output already exists')

    if not os.path.isfile(fileNameOut):
        os.system('file ' + fileNameOut)
        logging.error('problem with pdftotext, returning')
        return

    config = configparser.ConfigParser()
    config.read(os.path.join(parentDirectory, '..', 'config.ini'))
    RESET_BOW = config['PREPROCESSING'].getboolean('RESET_BOW')
    MANUAL_TOKENIZATION = config['PREPROCESSING'].getboolean('MANUAL_TOKENIZATION')

    if not os.path.isfile(fileNameOutBow) or RESET_BOW:
        if MANUAL_TOKENIZATION:
            bow.preprocess_text(fileNameOut, fileNameOutBow)
        else:
            bow.preprocess_gensim(fileNameOut, fileNameOutBow)
    
    return fileNameOutBow


def run(input_path, output_dir='./', overwrite=None):
    """Convert pdf(s) in input_path to pre Bag-of-word file(s).

    Args:
        input_path (str): File path or directory path containing pdfs
        output_dir (str): Location of where the output folder will be created
        overwrite (Boolean): Whether or not to re-process previously processed PDFs

    Returns:
        Filename of the output bag-of-word file. Bag-of-word file will be created in the outDIR folder

    """

    if os.path.isdir(input_path):
        logging.info('Parsing all pdfs in the directory %s', input_path)
        paths = []
        for f in glob(input_path + '/*'):
            # Only process pdf files
            if ispdf(f):
                bow_filename = pdf_bow(f, output_dir, overwrite=overwrite)
                paths.append(bow_filename)
            else:
                logging.info('not a pdf %s', f)
        return paths
    else:
        logging.info('Path %s not directory' % input_path)
        bow_filename = pdf_bow(input_path, output_dir, overwrite=overwrite)
        return bow_filename


if __name__ == '__main__':
    run("/Users/nus/git/tpms/pdf2bow/paper.pdf",
        output_dir='/Users/nus/git/tpms/pdf2bow/output',
        overwrite=True)
    '''
    command to run the file:
    python /Users/nus/git/tpms/pdf2bow/pdf2bow.py --input paper.pdf
    '''
