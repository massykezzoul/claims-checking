#!/usr/bin/env python3

from websites import fatabyyano as f
from websites import vishvasnews as v
from claim import Claim
import sys

sys.path.append("websites")


'''
    exec like this : 
    python3 __init__.py test_extraction/vishvas.csv test_extraction/vishvas.err
'''


def vishvas(argv):
    #claim_url = "https://www.vishvasnews.com/english/world/fact-check-no-this-is-not-the-image-of-an-indian-soldier/"
    vishvas = v.VishvasnewsFactCheckingSiteExtractor()

    file_name = ""
    err_file = ""
    if len(argv) > 1:
        file_name = argv[1]

        if len(argv) > 2:
            err_file = argv[2]

    vishvas.get_claim_and_print(file_name, err_file)


def fatabyyano(argv):
    fatabyyano = f.FatabyyanoFactCheckingSiteExtractor()

    file_name = ""
    err_file = ""
    if len(argv) > 1:
        file_name = argv[1]

        if len(argv) > 2:
            err_file = argv[2]

    fatabyyano.get_claim_and_print(file_name, err_file)


if __name__ == "__main__":
    # vishvas(sys.argv)
    vishvas = v.VishvasnewsFactCheckingSiteExtractor()

    review = vishvas.retrieve_listing_page_urls()

    print(review)
