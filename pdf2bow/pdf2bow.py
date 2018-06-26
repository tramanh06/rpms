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
#
#####################################################################

pdf2textCMD = "pdftotext"

# Other features to implement/think about:
#   - Extract title, abstract, citations
#   - Different inputs
#     - file containing URLs (say one per line)


def pdf_bow(pdfPath, localDir, pdfFile=None, stemmerCMD=None, overwrite=False):

    print '- %s:' % pdfPath,

    # some vars
    outDIR = localDir + "/output/"
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

    if not os.path.isfile(fileNameOutBow):
        bow.preprocess_text(fileNameOut, fileNameOutBow)


def run(input_path, output_dir='.', overwrite=None):
    '''
    Arguments:
    input_path: file path or directory path containing pdfs
    output_dir: location of where the output folder will be created
    overwrite: Boolean. whether or not to re-process previously processed PDFs
    '''

    if os.path.isdir(input_path):
        print 'Parsing all pdfs in the directory', input_path
        for f in glob(input_path + '/*'):
            # Only process pdf files
            if ispdf(f):
                pdf_bow(f, output_dir, overwrite=overwrite)
            else:
                print 'not a pdf', f
    else:
        print 'Path %s not directory' % input_path
        pdf_bow(input_path, output_dir, overwrite=overwrite)


if __name__ == '__main__':
    run("/Users/nus/git/tpms/pdf2bow/paper.pdf",
        output_dir='/Users/nus/git/tpms/pdf2bow/',
        overwrite=True)
    '''
    command to run the file:
    python /Users/nus/git/tpms/pdf2bow/pdf2bow.py --input paper.pdf
    '''
