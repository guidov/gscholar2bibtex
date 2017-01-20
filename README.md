gscholar2bibtex.py
==================

gscholar2bibtex.py is a Python module that implements a querier and parser for Google Scholar's output and returns a bibtex reference.

If you automate and repeat too fast, you will get blocked by Google and have to start the access process over again.

This is used to put you bibtex references together from a series of searches or PDFs


Features
--------

* Extracts bibtex reference from a google scholar search done with the CLI


Setup (using Chrome)
--------------------

-->With your chrome web browser go to:
https://scholar.google.ca/

--> Settings (top right)
    -->Bibliography manager

>Don't show any citation import links.

>Show links to import citations into BibTeX.

>Save Cancel

Check "Show links to import citations into BibTeX."

Then Save

This will save a cookie to your chrome browser

On Chrome
--> Settings
    --> Privacy
        --> Content Settings
            --> Cookies
                --> All cookies and site data

Search for scholar.google
    --> GSP

Copy "Name=Content" to your cookie file on disk (e.g. cookie_file.txt):
e.g.
GSP=IN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx:LD=en:CF=4:LM=xxxxxxxxxx:S=xxxxxxxxxxxxxxxx


Examples
--------

Try gscholar2bibtex.py --help for all available options.

Retrieve BibTeX entry article written by Einstein on quantum theory:

    $ gscholar2bibtex.py --phrase "albert einstein" --phrase gscholar2bibtex.py -c cookie_file.txt

Retrieve a BibTeX entry from a PDF file on disk.

    $ ./gscholar2bibtex.py -f my_paper.pdf -c cookie_file.txt


License
-------

gscholar2bibtex.py is using the standard [BSD license](http://opensource.org/licenses/BSD-2-Clause).
