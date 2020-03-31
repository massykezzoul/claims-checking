#!/usr/bin/env python3

from websites import fatabyyano as f
from websites import vishvasnews as v
from claim import Claim
import sys

sys.path.append("websites")


def vishvas():
    #claim_url = "https://www.vishvasnews.com/english/world/fact-check-no-this-is-not-the-image-of-an-indian-soldier/"
    vishvas = v.VishvasnewsFactCheckingSiteExtractor()

    print("claim, title, claim_author, links, date, tags, authors, rating_value")

    for retrieve_page in vishvas.retrieve_listing_page_urls():
        for claim_page in vishvas.retrieve_urls(vishvas.get(retrieve_page), retrieve_page, 0, 0):
            webpage = vishvas.get(claim_page)
            if vishvas.is_claim(webpage):
                claim = vishvas.extract_claim(webpage)
                title = vishvas.extract_title(webpage)
                claimeur = vishvas.extract_claimed_by(webpage)
                links = vishvas.extract_links(webpage)
                date = vishvas.extract_date(webpage)
                tags = vishvas.extract_tags(webpage)
                authors = vishvas.extract_author(webpage)
                rating = vishvas.extract_rating_value(webpage)

                print('"' + claim + '"', end=', ')
                print('"' + title + '"', end=', ')
                print('"' + claimeur + '"', end=', ')
                print('"' + str(links) + '"', end=', ')
                print('"' + date + '"', end=', ')
                print('"' + str(tags) + '"', end=', ')
                print('"' + str(authors) + '"', end=', ')
                print('"' + rating + '"', end='\n')


def fatabyyano():
    fatabyyano = f.FatabyyanoFactCheckingSiteExtractor()
    claims_urls = ["https://fatabyyano.net/%d8%a7%d9%86%d8%aa%d9%87%d8%aa-%d8%ad%d9%84%d9%88%d9%84-%d8%a7%d9%84%d8%a3%d8%b1%d8%b6-%d8%a7%d9%84%d8%a3%d9%85%d8%b1-%d9%85%d8%aa%d8%b1%d9%88%d9%83/"]

    # printing result
    for claim_url in claims_urls:
        claim_url.rstrip()  # enleve le dernier '\n' de la ligne
        webpage = fatabyyano.get(claim_url)
        claims = fatabyyano.extract_claim_and_review(webpage, claim_url)[0]


if __name__ == "__main__":
    vishvas()
