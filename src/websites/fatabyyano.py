# -*- coding: utf-8 -*-
import re
from typing import *

from bs4 import BeautifulSoup
from dateparser.search import search_dates
from tqdm import tqdm

import requests
from bs4 import NavigableString


class Claim:
    pass


class FatabyyanoFactCheckingSiteExtractor:

    def __init__(self):
        print("Configuration Here...")

    def get(self, url):
        """ @return the webpage """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        html = requests.get(url, headers=headers).text
        soup = BeautifulSoup(html, 'lxml')
        # removing some useless tags
        for s in soup.select("script, iframe, head, header, footer"):
            s.extract()
        return soup

    def get_all_claims(self):
        """ @retun all claims """
        claims = []
        return claims

    def retrieve_listing_page_urls(self) -> List[str]:
        """
            Abstract method. Retrieve the URLs of pages that allow access to a paginated list of claim reviews. This
            concerns some sites where all the claims are not listed from a single point of access but first
            categorized by another criterion (e.g. on politifact there is a separate listing for each possible rating).
            :return: Return a list of listing page urls
        """
        different_urls = []
        different_rating_value = ["صحيح","زائف-جزئياً","زائف","خادع","ساخر","رأي","عنوان-مضلل","غير-مؤهل"]
        url_begin = "https://fatabyyano.net/newsface/"
        for value in different_rating_value :
            different_urls.append(url_begin+value+"/")
        return different_urls

    def find_page_count(self, parsed_listing_page: BeautifulSoup) -> int:
        """
            A listing page is paginated and will sometimes contain information pertaining to the maximum number of pages
            there are. For sites that do not have that information, please return a negative integer or None
            :param parsed_listing_page:
            :return: The page count if relevant, otherwise None or a negative integer
        """
        page_numbers = parsed_listing_page.select(
            "div.nav-links a.page-numbers span")
        maximum = 1
        for page_number in page_numbers:
            p = int(page_number.text)
            if (p > maximum):
                maximum = p
        return maximum

<<<<<<< HEAD
    
    def retrieve_urls(self, parsed_claim_review_page: BeautifulSoup, listing_page_url: str, begin: int, number_of_pages: int) -> List[str]:
        url_begin = listing_page_url+"page/"
        url_end = "/"
=======
    def retrieve_urls(self, parsed_listing_page: BeautifulSoup, listing_page_url: str, begin: int, number_of_pages: int) \
            -> List[str]:
        """
            :parsed_listing_page: --> une page (parsed) qui liste des claims
            :listing_page_url:    --> l'url associé à la page ci-dessus
            :number_of_page:      --> number_of_page
            :return:              --> la liste des url de toutes les claims
        """
        url_begin = "https://fatabyyano.net/page/"
        url_end = "/?s"
>>>>>>> ad96d73e4fcdfab5904ec914c66134833d677a88
        result = []
        for page_number in range(begin, number_of_pages+1):
            url = url_begin+str(page_number)+url_end
            parsed_web_page = self.get(url)
            links = parsed_web_page.select("main article h2 a")
            for link in links:
                result.append(link['href'])
        return result



    def extract_claim_and_review(self, parsed_claim_review_page: BeautifulSoup, url: str) -> List[Claim]:
        """ I think that this method extract everything """
        pass

    def extract_claim(self, parsed_claim_review_page: BeautifulSoup) -> str:
        claim = parsed_claim_review_page.select_one("h1.post_title")
        if claim:
            return claim.text
        else:
            # print("something wrong in extracting claim")
            return ""

    def extract_review(self, parsed_claim_review_page: BeautifulSoup) -> str:
        return ""

    def extract_date(self, parsed_claim_review_page: BeautifulSoup) -> str:
        date = parsed_claim_review_page.select_one(
            "time.w-post-elm.post_date.entry-date.published")
        if date:
            return date['datetime'].split("T")[0]
        else:
            print("something wrong in extracting the date")
            return ""

    def extract_tags(self, parsed_claim_review_page: BeautifulSoup) -> List[str]:
        """
            :parsed_claim_review_page:  --> the parsed web page of the claim
            :return:                    --> return a list of tags that are related to the claim
        """
        tags_link = parsed_claim_review_page.select(
            "div.w-post-elm.post_taxonomy.style_simple a")
        tags = []
        for tag_link in tags_link:
            if tag_link and tag_link.text:
                tag = tag_link.text
                if tag[0] == '#':  # if the tag begin with '#'
                    tag = tag[1:]
                tags.append(tag)
        return tags

    def extract_author(self, parsed_claim_review_page: BeautifulSoup) -> str:
        return "fatabyyano"

    def extract_rating_value(self, parsed_claim_review_page: BeautifulSoup) -> str:
        btn = parsed_claim_review_page.select_one(
            "div.style_badge a.w-btn.us-btn-style_7")
        if btn:
            return btn.text
        else:
            # print("Something wrong in extracting rating value !")
            return ""

    def translate_rating_value(initial_rating_value: str) -> str:
        return {
            "صحيح": "TRUE",
            "زائف جزئياً": "MIXTURE",
            "عنوان مضلل": "MIXTURE",  # ?
            "رأي": "OTHER",  # ? (Opinion)
            "ساخر": "OTHER",  # ? (Sarcastique)
            "غير مؤهل": "FALSE",  # ? (Inéligible)
            "خادع": "FALSE",  # ? (Trompeur)
            "زائف": "FALSE"
        }[initial_rating_value]

        # return translate[initial_rating_value]
