#!/usr/bin/env python3

from websites import fatabyyano as f
import sys

sys.path.append("websites")


def main():
    print("main")
    fatabyyano = f.FatabyyanoFactCheckingSiteExtractor()

    print("url, rating, rating_translate, claim, date, tags, source, review")

    # retrieving claims urls
    # retrieve_listing_page_urls = fatabyyano.retrieve_listing_page_urls()
    """    for page in retrieve_listing_page_urls:
                page_parsed = fatabyyano.get(page)
                number_of_pages = fatabyyano.find_page_count(page_parsed)
                claims_urls = fatabyyano.retrieve_urls(
                    page_parsed, page, 1, number_of_pages)
    """
    claims_urls = ["https://fatabyyano.net/%d9%83%d9%88%d9%8a%d9%83%d8%a8-%d8%b3%d9%8a%d8%b5%d8%b7%d8%af%d9%85-%d8%a8%d8%a7%d9%84%d8%a3%d8%b1%d8%b6-%d9%81%d9%8a-29-%d8%a3%d8%a8%d8%b1%d9%8a%d9%84-%d9%88%d9%8a%d9%86%d9%87%d9%8a-%d8%a7%d9%84/"]
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
        print(escape(source))


def escape(str):
    # define this fucntion as a method of the class Fatabyyano...
    str = str.replace("ﷺ", "صَلَّىٰ ٱللَّٰهُ عَلَيْهِ وَسَلَّمَ").replace(
        "\n", " ").replace('"', "'")
    return '"' + str + '"'


if __name__ == "__main__":
    main()
