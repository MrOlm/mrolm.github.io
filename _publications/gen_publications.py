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

def main(args):
    fl = 'publications2.html'
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
title: Publications2
permalink: /publications2/
---
<script async src="https://badge.dimensions.ai/badge.js" charset="utf-8"></script>
<script type='text/javascript' src='https://d1bxh8uas1mnw7.cloudfront.net/assets/embed.js'></script>
'''
    )

    # Write the body
    Bdb = pd.read_csv(bib)
    for i, row in Bdb.sort_values('Date published', ascending=False).iterrows():
        out.write(row['Title'] + '\n')
        out.write('<span class="__dimensions_badge_embed__" data-doi={0} data-style="small_circle"></span>\n'.format(
            row['DOI']))
        out.write('<div class=\'altmetric-embed\' data-badge-type=\'donut\' data-doi="{0}"></div>\n'.format(
            row['DOI']))


    out.write(doc.getvalue())

    out.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # Required positional argument
    parser.add_argument("bibliography", help="Required bibliography")

    args = parser.parse_args()
    main(args)
