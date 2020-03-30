#!/usr/bin/env python3

from websites import fatabyyano as f
from websites import vishvasnews as v
from claim import Claim
import sys

sys.path.append("websites")


def vishvas():
    vishvas = v.VishvasnewsFactCheckingSiteExtractor()

    claim_url = "https://www.vishvasnews.com/english/world/fact-check-no-this-is-not-the-image-of-an-indian-soldier/?fbclid=IwAR0TG7zEzGhuHq19jcASWlfK8WPc2DQsV0g-Ki-43hOrS7pUfmqloPSL5dw/"
    webpage = vishvas.get(claim_url)
    title = vishvas.extract_title(webpage)
    claim = vishvas.extract_claim(webpage)
    rating = vishvas.extract_rating_value(webpage)
    authors = vishvas.extract_author(webpage)
    tags = vishvas.extract_tags(webpage)

    print('rating : "' + rating + '"')
    print('title : "' + title + '"')
    print('claim : "' + claim + '"')
    print('authors :' , *authors, sep = ", ")  
    print('tags :',*tags, sep=", ")
  


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
