" Small script to check if any file in the folder has length >1000000 (spacy nlp limit documents size to be less than 1mil) "

import glob
import utils

# directory = "bow/Bryan_Low/"
directory = "bow/Leong_Tze_Yun/"


all_texts = {filename: utils.read_file(filename) for filename in glob.glob(directory + '*.txt')}
length_texts = {filename: len(text) for filename, text in all_texts.iteritems()}
print filter(lambda (k, v): v > 1000000, length_texts.iteritems())