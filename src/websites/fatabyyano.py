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


class FatabyyanoFactCheckingSiteExtractor:

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
            "صحيح", "زائف-جزئياً", "زائف", "خادع", "ساخر", "رأي", "عنوان-مضلل", "غير-مؤهل"]
        url_begin = "https://fatabyyano.net/newsface/"
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
        page_numbers = parsed_listing_page.select(
            "div.nav-links a.page-numbers span")
        maximum = 1
        for page_number in page_numbers:
            p = int(page_number.text)
            if (p > maximum):
                maximum = p
        return maximum

    def retrieve_urls(self, parsed_claim_review_page: BeautifulSoup, listing_page_url: str, begin: int, number_of_pages: int) -> List[str]:
        """
            :parsed_listing_page: --> une page (parsed) qui liste des claims
            :listing_page_url:    --> l'url associé à la page ci-dessus
            :number_of_page:      --> number_of_page
            :return:              --> la liste des url de toutes les claims
        """
        url_begin = listing_page_url+"page/"
        url_end = "/"
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
        self.claim = self.extract_claim(parsed_claim_review_page)
        self.review = self.extract_review(parsed_claim_review_page)

        claim = Claim()
        claim.set_rating_value(
            self.extract_rating_value(parsed_claim_review_page))
        claim.set_alternate_name(FatabyyanoFactCheckingSiteExtractor.translate_rating_value(
            self.extract_rating_value(parsed_claim_review_page)))
        claim.set_source("fatabyyano")
        claim.set_author("fatabyyano")
        claim.setDatePublished(self.extract_date(parsed_claim_review_page))
        claim.set_claim(self.claim)
        claim.set_body(self.review)
        claim.set_refered_links(self.extract_links(parsed_claim_review_page))
        claim.set_title(self.extract_claim(parsed_claim_review_page))
        claim.set_date(self.extract_date(parsed_claim_review_page))
        claim.set_url(url)
        claim.set_tags(self.extract_tags(parsed_claim_review_page))
        # extract_entities returns two variables
        json_claim, json_body = self.extract_entities()
        claim.set_claim_entities(json_claim)
        claim.set_body_entities(json_body)

        return [claim]

    def extract_claim(self, parsed_claim_review_page: BeautifulSoup) -> str:
        claim = parsed_claim_review_page.select_one("h1.post_title")
        if claim:
            return claim.text
        else:
            # print("something wrong in extracting claim")
            return ""

    def extract_review(self, parsed_claim_review_page: BeautifulSoup) -> str:
        return parsed_claim_review_page.select_one(
            "section.l-section.wpb_row.height_small div[itemprop=\"text\"]").text

    def extract_links(self, parsed_claim_review_page: BeautifulSoup) -> str:
        links = ""
        links_tags = parsed_claim_review_page.select(
            "section.l-section.wpb_row.height_small div[itemprop=\"text\"] a")
        for link_tag in links_tags:
            if link_tag['href']:
                links += link_tag['href'] + ", "
        return links[:len(links)-1]

    def extract_date(self, parsed_claim_review_page: BeautifulSoup) -> str:
        date = parsed_claim_review_page.select_one(
            "time.w-post-elm.post_date.entry-date.published")
        if date:
            return date['datetime'].split("T")[0]
        else:
            print("something wrong in extracting the date")
            return ""

    def extract_tags(self, parsed_claim_review_page: BeautifulSoup) -> str:
        """
            :parsed_claim_review_page:  --> the parsed web page of the claim
            :return:                    --> return a list of tags that are related to the claim
        """
        tags_link = parsed_claim_review_page.select(
            "div.w-post-elm.post_taxonomy.style_simple a[rel=\"tag\"]")
        tags = ""
        for tag_link in tags_link:
            if tag_link.text:
                tag = (tag_link.text).replace("#", "")
                tags += tag + ","

        return tags[:len(tags)-1]

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

    def extract_entities(self):
        """
            You sould call extract_claim and extract_review method and 
            store the result in self.claim and self.review before calling this method
            :return: --> entities in the claim and the review in to different variable
        """
        return self.get_json_format(self.tagme(self.translate(self.claim))), self.get_json_format(self.tagme(self.translate(self.review)))

    @staticmethod
    def translate_rating_value(initial_rating_value: str) -> str:
        return {
            "صحيح": "TRUE",
            "زائف جزئياً": "MIXTURE",
            "عنوان مضلل": "OTHER",  # ?
            "رأي": "OTHER",  # ? (Opinion)
            "ساخر": "OTHER",  # ? (Sarcastique)
            "غير مؤهل": "FALSE",  # ? (Inéligible)
            "خادع": "FALSE",  # ? (Trompeur)
            "زائف": "FALSE"
        }[initial_rating_value]

    @staticmethod
    def translate(text):
        """
            :text:  --> The text in arabic
            :return:  --> return a translation of :text: in english
        """
        yandexAPI = 'trnsl.1.1.20200311T210815Z.796b747ff14857c9.2e7b856527d2689a26379ff56769f5b3c087f55b'
        yandex = YandexTranslate(yandexAPI)
        return yandex.translate(text, 'ar-en')['text'][0]

    @staticmethod
    def tagme(text):
        """
            :text:  --> The text in english after translation
            :return:  --> return a list of entities
        """
        tagme.GCUBE_TOKEN = "b6fdda4a-48d6-422b-9956-2fce877d9119-843339462"
        return tagme.annotate(text)

    # write this method (and tagme, translate) in an another file cause we can use it in other websites
    @staticmethod
    def get_json_format(tagme_entity):
        '''
            :tagme_entity: must be an object of AnnotateResposte Class returned by tagme function
        '''
        data_set = []
        i = 0
        min_rho = 0.1

        for annotation in tagme_entity.get_annotations(min_rho):
            entity = {}
            entity["id"] = annotation.entity_id
            entity["begin"] = annotation.begin
            entity["end"] = annotation.end
            entity["entity"] = annotation.entity_title
            entity["text"] = annotation.mention
            entity["score"] = annotation.score
            entity["categories"] = []
            if tagme_entity.original_json["annotations"][i]["rho"] > min_rho:
                for categorie in tagme_entity.original_json["annotations"][i]["dbpedia_categories"]:
                    entity["categories"].append(categorie)
            i = i + 1
            data_set.append(entity)

        return json.dumps(data_set)
