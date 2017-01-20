#!/usr/bin/env python
"""
This module provide a method for querying Google Scholar and returns bibtex results
"""
# ChangeLog
# ---------

import optparse
import sys
import re
from PyPDF2 import PdfFileReader
import unicodedata
import urllib.request
try:
    # python 2
    from htmlentitydefs import name2codepoint
except ImportError:
    # python 3
    from html.entities import name2codepoint


def get_links(html, outformat):
    """Return a list of reference links from the html."""
    if outformat == 4:
        # refre = re.compile(r'<a href="(/scholar\.bib\?[^"]*)')
        refre = re.compile(r'<a href="(https://scholar.googleusercontent.com/scholar\.bib\?[^"]*)')
    reflist = refre.findall(html)
    # escape html entities
    reflist = [re.sub('&(%s);' % '|'.join(name2codepoint), lambda m:
                      chr(name2codepoint[m.group(1)]), s) for s in reflist]
    return reflist


def webPageToText(url, browser):
    req = urllib.request.Request(url, headers=browser)
    con = urllib.request.urlopen(req)
    text = con.read().decode('utf8')
    return text


def main():
    usage = """gscholar2bibtex.py <options> <query string>
A command-line interface to output a single bibtex citation from Google Scholar.

Examples:

# Retrieve one article written by Einstein on quantum theory:
gscholar2bibtex.py -p "albert einstein" -p "quantum theory" -c cookie_file.txt
"""

    fmt = optparse.IndentedHelpFormatter(max_help_position=50, width=100)
    parser = optparse.OptionParser(usage=usage, formatter=fmt)
    parser.add_option('-p', '--phrases',
                      metavar='PHRASE',
                      default=[],
                      action='append',
                      help='Results must contain exact phrase or phrases')
    parser.add_option('-c', '--cookie-file',
                      metavar='FILE',
                      default=None,
                      help='File that contains google scholar cookie for your account')
    parser.add_option('-f', '--pdf',
                      metavar='FILE',
                      default=None,
                      help='PDF File to extract authors and title from for search')

    options, _ = parser.parse_args()

    # Show help if we have neither keyword search nor author name
    if len(sys.argv) == 1:
        parser.print_help()
        return 1

    if options.cookie_file is None:
        parser.print_help()
        return 1

    if options.pdf is None:
        # print("You requeseted the following phrases {}".format(options.phrases))
        phrase_list = '+'.join(options.phrases).replace(" ", "%20").replace(".", "")
    else:
        pdf_reader = PdfFileReader(options.pdf)
        pdf_title = pdf_reader.getDocumentInfo().title
        pdf_author = pdf_reader.getDocumentInfo().author
        pdf_authors = '+'.join(pdf_author.split('; '))
        phrase_list = (pdf_title+pdf_authors).replace(" ", "%20").replace(".", "")
        phrase_list = re.sub(u"\u2013", "-", phrase_list)
        # phrase_list = unicodedata.normalize('NFKD', phrase_list).encode('ascii','ignore')
        # print("You requeseted the following phrases {}".format(phrase_list))

    urlhead = 'https://scholar.google.com/scholar?start=0&num=1&q='
    urltail = '&hl=en'
    url = urlhead+phrase_list+urltail

    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
    with open(options.cookie_file, 'r') as mycookiefile:
        my_cookie = mycookiefile.read().replace('\n', '')
    headers = {'User-Agent': user_agent, 'Cookie': my_cookie}

    req = urllib.request.Request(url, headers=headers)
    con = urllib.request.urlopen(req)
    html = con.read().decode('utf8')
    linklist = get_links(html, 4)

    bibtex = webPageToText(linklist[0], headers)
    print(bibtex)

if __name__ == "__main__":
    sys.exit(main())
