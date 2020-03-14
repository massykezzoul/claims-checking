#!/usr/bin/env python3

from websites import fatabyyano as f
from claim import Claim
import sys

sys.path.append("websites")


def main():
    fatabyyano = f.FatabyyanoFactCheckingSiteExtractor()
    claims_urls = ["https://fatabyyano.net/%d9%83%d9%88%d9%8a%d9%83%d8%a8-%d8%b3%d9%8a%d8%b5%d8%b7%d8%af%d9%85-%d8%a8%d8%a7%d9%84%d8%a3%d8%b1%d8%b6-%d9%81%d9%8a-29-%d8%a3%d8%a8%d8%b1%d9%8a%d9%84-%d9%88%d9%8a%d9%86%d9%87%d9%8a-%d8%a7%d9%84/"]

    # printing result
    for claim_url in claims_urls:
        claim_url.rstrip()  # enleve le dernier '\n' de la ligne
        webpage = fatabyyano.get(claim_url)
        claims = fatabyyano.extract_claim_and_review(webpage, claim_url)[0]

        print(claims.get_claim_entities().replace(" , ", "\n") + "\n" +
              claims.get_body_entities().replace(" , ", "\n"))


def escape(str):
    # define this fucntion as a method of the class Fatabyyano...
    str = str.replace("ﷺ", "صَلَّىٰ ٱللَّٰهُ عَلَيْهِ وَسَلَّمَ").replace(
        "\n", " ").replace('"', "'")
    return '"' + str + '"'


if __name__ == "__main__":
    main()
