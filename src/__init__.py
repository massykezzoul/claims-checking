#!/usr/bin/env python3

from websites import fatabyyano as f
import sys

sys.path.append("websites")


def main():
    print("main")
    fatabyyano = f.FatabyyanoFactCheckingSiteExtractor()

    print("url, rating, rating_translate, claim, date, tags")

    # retrieving claims urls
    retrieve_listing_page_urls = fatabyyano.retrieve_listing_page_urls()

    for page in retrieve_listing_page_urls:
        page_parsed = fatabyyano.get(page)
        number_of_pages = fatabyyano.find_page_count(page_parsed)
        claims_urls = fatabyyano.retrieve_urls(
            page_parsed, page, 1, number_of_pages)

        # printing result
        for claim_url in claims_urls:
            claim_url.rstrip()  # enleve le dernier '\n' de la ligne
            webpage = fatabyyano.get(claim_url)
            rating = fatabyyano.extract_rating_value(webpage)
            claim = fatabyyano.extract_claim(webpage)
            date = fatabyyano.extract_date(webpage)
            tags = fatabyyano.extract_tags(webpage)
            rating_translate = f.FatabyyanoFactCheckingSiteExtractor.translate_rating_value(
                rating)
            print(claim_url+", "+rating+", "+rating_translate +
                  ", "+claim + ", "+date+", \""+tags+"\"")


if __name__ == "__main__":
    main()
