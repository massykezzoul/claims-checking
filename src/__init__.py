#!/usr/bin/env python3

from websites import fatabyyano as f
import sys

sys.path.append("websites")


def main():
    print("main")
    fatabyyano = f.FatabyyanoFactCheckingSiteExtractor()

    print("url, rating, rating_translate, claim, date, tags, source, review")

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
            source = fatabyyano.extract_links(webpage)
            review = fatabyyano.extract_review(webpage)
            rating_translate = f.FatabyyanoFactCheckingSiteExtractor.translate_rating_value(
                rating)
            print(escape(claim_url)+", "+escape(rating)+", "+rating_translate +
                  ", "+escape(claim) + ", "+date+", "+escape(tags)+", "+escape(source)+", "+escape(review))


def escape(str):
    # define this fucntion as a method of the class Fatabyyano...
    str = str.replace("ﷺ", "صَلَّىٰ ٱللَّٰهُ عَلَيْهِ وَسَلَّمَ").replace(
        "\n", " ").replace('"', "'")
    return '"' + str + '"'


if __name__ == "__main__":
    main()
