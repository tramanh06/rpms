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

sys.path += ['.']


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

    print '- %s:' % pdfPath,

    # Check if out folder exists, create otherwise
    utils.is_folder_exists_create_otherwise(outDIR)

    if pdfFile is None:
        if not os.path.isdir(outDIR):
            try:
                os.mkdir(outDIR)
            except OSError, e:
                print 'ERROR: Problem creating directory...'
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
        print 'converting (%s %s -> %s)' % (pdf2textCMD, pdfPath, fileNameOut)
        os.system(""" %s "%s" "%s" """ % (pdf2textCMD, pdfPath, fileNameOut))
    else:
        print 'not converting since output already exists'

    if not os.path.isfile(fileNameOut):
        os.system('file ' + fileNameOut)
        print 'problem with pdftotext, returning'
        return

    # if not os.path.isfile(fileNameOutBow):
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
        print 'Parsing all pdfs in the directory', input_path
        paths = []
        for f in glob(input_path + '/*'):
            # Only process pdf files
            if ispdf(f):
                bow_filename = pdf_bow(f, output_dir, overwrite=overwrite)
                paths.append(bow_filename)
            else:
                print 'not a pdf', f
        return paths
    else:
        print 'Path %s not directory' % input_path
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
