#!/usr/bin/env python

# Version 0.1
# Matt Olm
# mattolm@berkeley.edu
# 02.20.19
'''
The purpose of this script is to take the PaperPile bibliography and generate
an html publications page
'''

__author__ = "Matt Olm"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
import pandas as pd
import numpy as np

def main(args):
    fl = 'publications.html'
    bib = args.bibliography
    gen_html_bib(bib, fl)

def gen_html_bib(bib, fl):
    from yattag import Doc
    doc, tag, text = Doc().tagtext()
    out = open(fl, 'w')

    # Write header
    out.write(
'''---
layout: post
title: Publications
permalink: /publications/
---
<script async src="https://badge.dimensions.ai/badge.js" charset="utf-8"></script>
<script type='text/javascript' src='https://d1bxh8uas1mnw7.cloudfront.net/assets/embed.js'></script>


<a href="https://scholar.google.com/citations?user=BoDUkpMAAAAJ&hl"><big>Link to google scholar</big></a>
</br>
</br>
'''
    )

    # Write the body
    Bdb = pd.read_csv(bib)
    for i, row in Bdb.sort_values('Date published', ascending=False).iterrows():
        # make this a paragraph
        #out.write('<p style="border: 1px solid black; width: 100%" >\n')
        #out.write('<p style="overflow: auto">\n')
        out.write('<p>\n')

        citation = gen_html_citation(row)
        out.write("<body> {0} </body>\n".format(citation))
        #out.write("<body style=\"display:inline-block\"> {0} </body>\n".format(citation))

        out.write('<span style="display:block">\n')
        out.write('<span style="display:inline" class=\'altmetric-embed\' data-badge-type=\'donut\' data-doi="{0}"></span>\n'.format(
            row['DOI']))
        # out.write('<span style="display:inline" class="__dimensions_badge_embed__" data-doi={0} data-style="small_circle"></span>\n'.format(
        #     row['DOI']))
        out.write('<span style="display:inline" class="__dimensions_badge_embed__" data-doi={0} data-style="small_circle" data-hide-zero-citations="true"></span>\n'.format(
            row['DOI']))
        out.write('</span>\n')

        # out.write('<span class="__dimensions_badge_embed__" data-doi={0} data-style="small_circle"></span>\n'.format(
        #     row['DOI']))
        # out.write('<span class=\'altmetric-embed\' data-badge-type=\'donut\' data-doi="{0}"></span>\n'.format(
        #     row['DOI']))



        # close the paragraph
        out.write('\n</p>\n')
        out.write('\n<hr/>\n')



    out.write(doc.getvalue())

    out.close()

def gen_html_citation(row):
    '''
    From a row, generate the citation
    '''
    authors = row['Authors']
    authors = ', '.join([_add_dots(x) for x in authors.split(',')])
    authors = authors.replace('Olm M.R.', '<b>Olm M.R.</b>').replace(',', ', ')

    journal = row['Full journal']
    if str(journal) == 'nan':
        journal = row['Journal']
    if str(journal) == 'nan':
        journal = row['Source']

    # The regular format I was using
    cit = "{0} ({2}). <i>{1}</i>. <b>{3}</b>".format(authors,
            row['Title'].replace('{','').replace('}',''),
            row['Publication year'],
            journal)

    # Crazy new format
    pub = "<a href=\"{1}\"> {0}</a>".format(row['Title'].replace('{','').replace('}',''),
            row['URLs'].split(';')[0])

    #cit = "<i><big>{1}</i> - <b>{3}</b> ({2})</big><br/>{0}".format(
    cit = "<i>{1}</i> - <b>{3}</b> ({2})<br/>{0}".format(
            authors,
            pub,
            row['Publication year'],
            journal)
    return cit

def _add_dots(x):
    second = '.'.join(x.split()[-1])
    return ' '.join(x.split()[:-1]) + ' ' + second + '.'

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # Required positional argument
    parser.add_argument("bibliography", help="Required bibliography")

    args = parser.parse_args()
    main(args)
