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
import json


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
            s.decompose()
        return soup

    def post(self, url, data):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        html = requests.post(url, data=data, header=headers).text
        soup = BeautifulSoup(html, 'lxml')
        # removing some useless tags
        for s in soup.select("script, iframe, head, header, footer, style"):
            s.decompose()
        return soup

    def retrieve_listing_page_urls(self) -> List[str]:
        """
            Abstract method. Retrieve the URLs of pages that allow access to a paginated list of claim reviews. This
            concerns some sites where all the claims are not listed from a single point of access but first
            categorized by another criterion (e.g. on politifact there is a separate listing for each possible rating).
            :return: Return a list of listing page urls
        """
        different_urls = []
        different_categories_value = [
            "politics", "society", "world", "viral", "health"]
        url_begin = "https://www.vishvasnews.com/english/"
        for value in different_categories_value:
            different_urls.append(url_begin+value+"/")
        return different_urls

    def find_page_count(self, parsed_listing_page: BeautifulSoup) -> int:
        """
            A listing page is paginated and will sometimes contain information pertaining to the maximum number of pages
            there are. For sites that do not have that information, please return a negative integer or None
            :param parsed_listing_page:
            :return: The page count if relevant, otherwise None or a negative integer
        """
        return -1

    def retrieve_urls(self, parsed_listing_page: BeautifulSoup, listing_page_url: str, begin: int, number_of_pages: int) -> List[str]:
        """
            :parsed_listing_page: --> une page (parsed) qui liste des claims
            :listing_page_url:    --> l'url associé à la page ci-dessus
            :number_of_page:      --> number_of_page
            :return:              --> la liste des url de toutes les claims
        """
        links = []
        select_links = 'ul.listing li div.imagecontent h3 a'
        # links in the static page
        claims = parsed_listing_page.select(
            "div.ajax-data-load " + select_links)
        for link in claims:
            if link["href"]:
                links.append(link["href"])

        # for links loaded by AJAX
        r = re.compile(
            "https://www.vishvasnews.com/(.*)/(.*)[/]").match(listing_page_url)

        lang = r.group(1)
        categorie = r.group(2)

        url_ajax = "https://www.vishvasnews.com/wp-admin/admin-ajax.php"
        data = {
            'action': 'ajax_pagination',
            'query_vars': '{"category_name" : "' + categorie + '", "lang" : "' + lang + '"}',
            'page': 1,
            'loadPage': 'file-archive-posts-part'
        }

        response = self.post(url_ajax, data)

        while True:
            claims = response.select(select_links)
            for link in claims:
                if link['href']:
                    links.append(link['href'])

            if response.find("nav"):
                data['page'] = data['page'] + 1
                response = self.post(url_ajax, data)
                continue
            else:
                break

        return links

    def extract_claim_and_review(self, parsed_claim_review_page: BeautifulSoup, url: str) -> List[Claim]:
        return [claim]

    def extract_claim(self, parsed_claim_review_page: BeautifulSoup) -> str:
        claim = parsed_claim_review_page.find("ul", class_="claim-review")
        if claim:
            return claim.li.span.text
        else:
            return ""

    def extract_title(self, parsed_claim_review_page: BeautifulSoup) -> str:
        title = parsed_claim_review_page.find("h1", class_="article-heading")
        if title:
            return title.text.strip()
        else:
            return ""

    def extract_review(self, parsed_claim_review_page: BeautifulSoup) -> str:
        return

    def extract_links(self, parsed_claim_review_page: BeautifulSoup) -> str:

        links = []
        # extracting the main article body
        review_body = parsed_claim_review_page.select_one(
            "div.lhs-area")
        # removing the social-media sahres links
        review_body.select_one('ul.social-icons-details').decompose()

        # removing authors  & tag  links
        b = False

        # ( > * ) ==> direct children in css
        for tag in review_body.select("> *"):
            if tag.get('class') and "reviews" in tag.get('class'):
                b = True
            if b:
                tag.decompose()
            else:
                continue
        # extracting links
        for link_tag in review_body.select('a'):
            if link_tag.has_attr('href'):
                links.append(link_tag['href'])

        return links

    def extract_date(self, parsed_claim_review_page: BeautifulSoup) -> str:
        date = parsed_claim_review_page.select("ul.updated li")[1]
        if date:
            return date.text.strip()
        else:
            return ""

        return

    def extract_tags(self, parsed_claim_review_page: BeautifulSoup) -> str:
        """
            : parsed_claim_review_page: - -> the parsed web page of the claim
            : return: - -> return a list of tags that are related to the claim
        """

        tags_link = parsed_claim_review_page.select(
            "ul.tags  a[rel=\"tag\"]")
        tags = ""
        for tag_link in tags_link:
            if tag_link.text:
                tag = (tag_link.text).replace("#", "")
                tags += tag + ","

        return tags[:len(tags)-1]
        return

    def extract_author(self, parsed_claim_review_page: BeautifulSoup) -> str:

        authors = []

        for author in parsed_claim_review_page.find_all("li", class_="name"):
            authors.append(author.a.text)
        if authors:
            return authors
        else:
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
            : text: - -> The text in arabic
            : return: - -> return a translation of: text: in english
        """

        return

    @staticmethod
    def tagme(text):
        """
            : text: - -> The text in english after translation
            : return: - -> return a list of entities
        """
        return

    # write this method (and tagme, translate) in an another file cause we can use it in other websites
    @staticmethod
    def get_json_format(tagme_entity):

        return
