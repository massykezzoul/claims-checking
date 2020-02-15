#!/usr/bin/env python3

from websites import fatabyyano as f
import sys

sys.path.append("websites")


def main():
    print("main")
    fatabyyano = f.FatabyyanoFactCheckingSiteExtractor()

    """ 
    retrieve_listing_page_urls = fatabyyano.retrieve_listing_page_urls()
    number_of_page = fatabyyano.find_page_count(fatabyyano.get(retrieve_listing_page_urls[0]))
    claims_url = fatabyyano.retrieve_urls(fatabyyano.get(retrieve_listing_page_urls[0]),retrieve_listing_page_urls[0],number_of_page) # takes 4 min
    for url in claims_url:
        print(url) 
    """

    claims_url = ["https://fatabyyano.net/%d9%81%d9%8a%d8%af%d9%8a%d9%88-%d9%87%d8%ac%d9%88%d9%85-%d8%a3%d8%b3%d8%b1%d8%a7%d8%a8-%d9%85%d9%86-%d8%b7%d8%a7%d8%a6%d8%b1-%d8%a7%d9%84%d8%ba%d8%b1%d8%a7%d8%a8-%d9%88-%d8%a7%d9%84%d8%a8%d8%b9%d9%88/", "https://fatabyyano.net/%d8%a5%d8%b3%d9%84%d8%a7%d9%85_%d8%a7%d9%84%d8%b5%d9%8a%d9%86_%d9%83%d9%88%d8%b1%d9%88%d9%86%d8%a7_%d8%a7%d9%84%d9%85%d8%b3%d9%84%d9%85%d9%8a%d9%86/", "https://fatabyyano.net/%d9%85%d8%a7-%d8%ad%d9%82%d9%8a%d9%82%d8%a9-%d9%81%d9%8a%d8%af%d9%8a%d9%88-%d8%b3%d9%85%d8%a7%d8%ad-%d8%a7%d9%84%d8%ad%d9%83%d9%88%d9%85%d8%a9-%d8%a7%d9%84%d8%b5%d9%8a%d9%86%d9%8a%d8%a9/", "https://fatabyyano.net/%d8%a7%d9%84%d8%aa%d9%8a%d8%b1%d9%85%d9%88%d8%b3_%d8%a7%d9%84%d8%b3%d8%b1%d8%b7%d8%a7%d9%86_%d8%a7%d9%84%d8%a3%d8%b3%d8%a8%d9%8a%d8%b3%d8%aa%d9%88%d8%b3_%d9%82%d9%87%d9%88%d8%a9_%d8%b4%d8%a7%d9%8a/",
                  "https://fatabyyano.net/%d8%a7%d9%84%d8%b5%d9%8a%d9%86_%d8%a7%d9%84%d8%ae%d9%86%d8%a7%d8%b2%d9%8a%d8%b1_%d8%a7%d9%84%d8%b7%d9%8a%d9%88%d8%b1_%d9%82%d9%8a%d8%b1%d9%88%d8%b3_%d9%83%d9%88%d8%b1%d9%88%d9%86%d8%a7_%d8%a7/", "https://fatabyyano.net/%d9%81%d9%8a%d8%b1%d9%88%d8%b3-%d9%83%d9%88%d8%b1%d9%88%d9%86%d8%a7-%d9%8a%d8%ac%d8%aa%d8%a7%d8%ad-%d9%85%d9%86%d8%a7%d8%b7%d9%82-%d8%a7%d9%84%d8%b5%d9%8a%d9%86-%d8%b9%d8%af%d8%a7-%d9%85%d9%86/", "https://fatabyyano.net/%d8%b2%d9%8a%d8%a7%d8%b1%d8%a9-%d8%b1%d8%a6%d9%8a%d8%b3-%d9%88%d8%b2%d8%b1%d8%a7%d8%a1-%d8%a7%d9%84%d8%b5%d9%8a%d9%86-%d9%84%d8%a3%d8%ad%d8%af-%d8%a7%d9%84%d9%85%d8%b3%d8%a7%d8%ac%d8%af/", "https://fatabyyano.net/%d9%85%d8%a7-%d8%ad%d9%82%d9%8a%d9%82%d8%a9-%d8%b2%d9%8a%d8%a7%d8%b1%d8%a9-%d8%b1%d8%a6%d9%8a%d8%b3-%d8%a7%d9%84%d8%b5%d9%8a%d9%86-%d8%a3%d8%ad%d8%af-%d9%85%d8%b3%d8%a7%d8%ac%d8%af-%d8%a7%d9%84%d9%85/"]
    different_rating_value = []

    for line in sys.stdin:
        line.rstrip()
        value = fatabyyano.extract_rating_value(fatabyyano.get(line))
        print(value)
        if value not in different_rating_value:
            different_rating_value.append(value)

    print("# Rating value system of fatabyyano : ")
    for v in different_rating_value:
        print("- " + str(v))


if __name__ == "__main__":
    main()
