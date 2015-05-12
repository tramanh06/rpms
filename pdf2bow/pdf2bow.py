import argparse
import codecs
from glob import glob
import os
import re
import sys

sys.path += ['.'] 

from sanitize import sanitize, tokenize, isUIWord
from ispdf import ispdf

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

pdf2textCMD="pdftotext"

# Other features to implement/think about: 
#   - Extract title, abstract, citations
#   - Different inputs
#     - file containing URLs (say one per line)

def makeBow(fileIn, fileOut, bow=None, verbose=False):

  if bow is None:
    bow = {}

  f = open(fileIn, 'r')
  if not f:
    print 'problem opening file'
    return None

  # token-ize lines 
  lines = f.readlines()
  f.close()

  # Remove equations and other things like that  
  for line in lines: 

    # replace accents
    words = tokenize(line)

    for word in words:
      word = word.lower()
      if len(word) > 0:
        if not isUIWord(word): # only keep informative words
          if word not in bow: 
              bow[word] = 0
          bow[word] = bow[word]+1


  f = open(fileOut, 'w')
  for k,v in bow.iteritems():
    #print '%s %s ' % (k v)
    f.write('%s %s\n' % (k, v))
    if verbose: 
      print k, v
      print len(bow)
  f.close()

  return bow


def pdf_bow(pdfPath, localDir, pdfFile=None, stemmerCMD=None, overwrite=False): 

  print '- %s:' % pdfPath, 

  # some vars 
  outDIR=localDir+"/"; 

  if pdfFile is None:
    if not os.path.isdir(outDIR):
      try:
        os.mkdir(outDIR)
      except OSError, e: 
        print 'ERROR: Problem creating directory...'
        raise 
    pdfFile = os.path.basename(pdfPath)
    if re.search('\.[a-zA-Z0-9]{1,4}', pdfFile):
        fileNameOut   =outDIR+re.sub('\.[a-zA-Z0-9]{1,4}$', '.txt', pdfFile)
        fileNameOutBow=outDIR+re.sub('\.[a-zA-Z1-9]{1,4}$', '.bow', pdfFile)
    else: 
        fileNameOut   =outDIR+pdfFile+'.txt'
        fileNameOutBow=outDIR+pdfFile+'.bow'
  else: 
    fileNameOut   =outDIR+pdfFile+'.txt'
    fileNameOutBow=outDIR+pdfFile+'.bow'

  # get text
  if not os.path.isfile(fileNameOut) or os.path.getsize(fileNameOut) == 0 or overwrite:
    print 'converting (%s %s -> %s)' % (pdf2textCMD, pdfPath, fileNameOut)
    os.system(""" %s "%s" "%s" """ % (pdf2textCMD, pdfPath, fileNameOut))
  else:
    print 'not converting since output already exists'

  if not os.path.isfile(fileNameOut):
    os.system('file '+fileNameOut)
    print 'problem with pdftotext, returning'
    return 

  # stem file
  if stemmerCMD is not None: 
    suffix = '.stemmed'
    os.system("%s '%s' > '%s'" % (stemCMD, fileNameOut, fileNameOut+suffix))
    fileNameOutStemmed = fileNameOut+suffix
    fileNameOutBowStemmed = fileNameOutBow+suffix

  if not os.path.isfile(fileNameOutBow): 
      makeBow(fileNameOut, fileNameOutBow)
  if stemmerCMD is not None: 
      makeBow(fileNameOutStemmed, fileNameOutBowStemmed)


def parse_args():

  parser = argparse.ArgumentParser(description='pdf2bow')
  parser.add_argument('--output_dir', type=str, required=False, default='.', help="output directory") 
  parser.add_argument('--input', type=str, required=True, help="input PDF or directory")
  parser.add_argument('--overwrite', type=bool, required=False, help="whether or not to re-process previously process PDFs", default=False)

  args = parser.parse_args()

  return args 


def run(): 

  args = parse_args()

  ## make sure stemming is there 
  #stemmerCMD = os.path.dirname(sys.argv[0])+'./stemming'
  #stemmerCMD = './stemming'
  #if not os.path.isfile(stemmerCMD): 
  #  print 'Compiling stemmer'
  #  print 'gcc -o stemming '+ stemmerCMD + '.c'
  #  os.system('gcc -o stemming '+ stemmerCMD + '.c')
  #  if not os.path.isfile(stemmerCMD):
  #    print 'Cannot compile stemmer, aborting'

  if os.path.isdir(args.input):
    print 'Parsing all pdfs in the directory', args.input
    for f in glob(args.input+'/*'): 
      # Only process pdf files
      if ispdf(f): 
        pdf_bow(f, args.output_dir, overwrite=args.overwrite)
      else:
        print 'not a pdf', f
  else:
    print 'Path %s not directory' % args.input
    pdf_bow(args.input, args.output_dir, overwrite=args.overwrite)
  

if __name__ == '__main__':
  run()
