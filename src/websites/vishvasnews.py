# -*- coding: utf-8 -*-
import re
from typing import *
import sys

from bs4 import BeautifulSoup
from dateparser.search import search_dates
from tqdm import tqdm

import requests
from bs4 import NavigableString

from claim import Claim
from yandex_translate import YandexTranslate
import json

import tagme

sys.path.append("../tagme")


class VishvasnewsFactCheckingSiteExtractor:

    def __init__(self):
        # Configuration Here...
        self.claim = ""
        self.review = ""
        pass

    def get(self, url):
        """ @return the webpage """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        html = requests.get(url, headers=headers).text
        soup = BeautifulSoup(html, 'lxml')
        # removing some useless tags
        for s in soup.select("script, iframe, head, header, footer, style"):
            s.extract()
        return soup

    def retrieve_listing_page_urls(self) -> List[str]:
        """
            Abstract method. Retrieve the URLs of pages that allow access to a paginated list of claim reviews. This
            concerns some sites where all the claims are not listed from a single point of access but first
            categorized by another criterion (e.g. on politifact there is a separate listing for each possible rating).
            :return: Return a list of listing page urls
        """
        different_urls = []
        different_rating_value = [
            "True", "Misleading","False"]
        url_begin = ""
        for value in different_rating_value:
            different_urls.append(url_begin+value+"/")
        return different_urls

    def find_page_count(self, parsed_listing_page: BeautifulSoup) -> int:
        """
            A listing page is paginated and will sometimes contain information pertaining to the maximum number of pages
            there are. For sites that do not have that information, please return a negative integer or None
            :param parsed_listing_page:
            :return: The page count if relevant, otherwise None or a negative integer
        """
        return 

    def retrieve_urls(self, parsed_claim_review_page: BeautifulSoup, listing_page_url: str, begin: int, number_of_pages: int) -> List[str]:
        """
            :parsed_listing_page: --> une page (parsed) qui liste des claims
            :listing_page_url:    --> l'url associé à la page ci-dessus
            :number_of_page:      --> number_of_page
            :return:              --> la liste des url de toutes les claims
        """
       
        return r

    def extract_claim_and_review(self, parsed_claim_review_page: BeautifulSoup, url: str) -> List[Claim]:
        """ I think that this method extract everything """

        return [claim]

    def extract_claim(self, parsed_claim_review_page: BeautifulSoup) -> str:
        claim = parsed_claim_review_page.find(div , class_=lhs-area)

        return 

    def extract_title(self, parsed_claim_review_page : BeautifulSoup) -> str:
        title = parsed_claim_review_page.find(h1 , class_=article-heading)
        if title:
            return title.text
        else:
            return ""


    def extract_review(self, parsed_claim_review_page: BeautifulSoup) -> str:
        return 

    def extract_links(self, parsed_claim_review_page: BeautifulSoup) -> str:
        links = []
        links_tags = parsed_claim_review_page.find(div , class_=lhs-area)
        
        for link_tag in links_tags.findAll('a', href=True):
                links.append(link_tag['href']+",")
                
        return links
       

    def extract_date(self, parsed_claim_review_page: BeautifulSoup) -> str:

        return 

    def extract_tags(self, parsed_claim_review_page: BeautifulSoup) -> str:
        """
            :parsed_claim_review_page:  --> the parsed web page of the claim
            :return:                    --> return a list of tags that are related to the claim
        """


        return 

    def extract_author(self, parsed_claim_review_page: BeautifulSoup) -> str:
        return ""

    def extract_rating_value(self, parsed_claim_review_page: BeautifulSoup) -> str:
          btn = parsed_claim_review_page.select_one(
            "div.selected span")
        if btn:
            return btn.text
        else: 
            return ""
            
    def extract_entities(self):
        
        return


    @staticmethod
    def translate(text):
        """
            :text:  --> The text in arabic
            :return:  --> return a translation of :text: in english
        """
       
        return

    @staticmethod
    def tagme(text):
        """
            :text:  --> The text in english after translation
            :return:  --> return a list of entities
        """
       
        return 

    # write this method (and tagme, translate) in an another file cause we can use it in other websites
    @staticmethod
    def get_json_format(tagme_entity):
        

        return 