# This Python file uses the following encoding: utf-8
import re
import unicodedata

############################
# Helper file for pdf2bow
############################


def sanitize(w):
    """ 
    sanitize (remove accents and standardizes) 
    """

    # print w

    map = {'æ': 'ae',
           'ø': 'o',
           '¨': 'o',
           'ß': 'ss',
           'Ø': 'o',
           '\xef\xac\x80': 'ff',
           '\xef\xac\x81': 'fi',
           '\xef\xac\x82': 'fl'}

    # This replaces funny chars in map
    for char, replace_char in map.iteritems():
        w = re.sub(char, replace_char, w)

    # w = unicode(w, encoding='latin-1')
    w = unicode(w, encoding='utf-8', errors='ignore')
    # w = w.encode('utf-8').strip()

    # This gets rid of accents
    w = ''.join((c for c in unicodedata.normalize(
        'NFD', w) if unicodedata.category(c) != 'Mn'))

    return w
