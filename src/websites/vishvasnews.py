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
import tagme
import copy  # to clone beautifulSoup nodes
import calendar  # convert month name to month number

sys.path.append("../tagme")


class VishvasnewsFactCheckingSiteExtractor:
    TAGME_API_KEY = 'b6fdda4a-48d6-422b-9956-2fce877d9119-843339462'

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
        html = requests.post(url, data=data, headers=headers).text
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

    def is_claim(self, parsed_claim_review_page: BeautifulSoup) -> bool:
        rating_value = parsed_claim_review_page.select_one(
            "div.selected span")
        return bool(rating_value)

    def extract_claim(self, parsed_claim_review_page: BeautifulSoup) -> str:
        claim = parsed_claim_review_page.find("ul", class_="claim-review")
        # check that the claim is in english
        if claim:
            return self.escape(claim.li.span.text)
        else:
            return ""

    def extract_title(self, parsed_claim_review_page: BeautifulSoup) -> str:
        title = parsed_claim_review_page.find("h1", class_="article-heading")
        if title:
            return self.escape(title.text.strip())
        else:
            return ""

    def extract_review(self, parsed_claim_review_page: BeautifulSoup) -> str:
        review = ""
        paragraphs = parsed_claim_review_page.select("div.lhs-area > p")

        for paragraph in paragraphs:
            review += paragraph.text + " "

        return self.escape(review)

    def extract_claimed_by(self, parsed_claim_review_page: BeautifulSoup) -> str:
        infos = []

        review = parsed_claim_review_page.find("ul", class_="claim-review")
        for info in review.find_all("li"):
            infos.append(info.span.text)

        if infos[1]:
            return self.escape(infos[1])
        else:
            return ""

    def extract_links(self, parsed_claim_review_page: BeautifulSoup) -> list:
        links = []

        # extracting the main article body
        review_body = parsed_claim_review_page.select_one(
            "div.lhs-area")
        # making a clone
        review_body = copy.copy(review_body)

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
        date = parsed_claim_review_page.select("ul.updated li")[1].text.strip()

        r = re.compile(
            '^Updated: *([a-zA-Z]+) ([0-9]+), ([0-9]{4})$').match(date)

        month = str({v: k for k, v in enumerate(
            calendar.month_name)}[r.group(1)])
        day = r.group(2)
        year = r.group(3)

        date = year + '-' + month + '-' + day

        if date:
            return date
        else:
            return ""

        return

    def extract_tags(self, parsed_claim_review_page: BeautifulSoup) -> list:
        """
            : parsed_claim_review_page: - -> the parsed web page of the claim
            : return: - -> return a list of tags that are related to the claim
        """

        tags_link = parsed_claim_review_page.select(
            "ul.tags a")
        tags = []
        for tag_link in tags_link:
            if tag_link.text:
                tags.append((tag_link.text).replace("#", ""))

        return tags
        return

    def extract_author(self, parsed_claim_review_page: BeautifulSoup) -> list:
        authors = []

        for author in parsed_claim_review_page.find_all("li", class_="name"):
            authors.append(author.a.text)

        return authors

    def extract_rating_value(self, parsed_claim_review_page: BeautifulSoup) -> str:
        btn = parsed_claim_review_page.select_one(
            "div.selected span")
        if btn:
            return btn.text.strip()
        else:
            return ""

    def extract_entities(self, claim: str, review: str):
        """
            You should call extract_claim and extract_review method and
            store the result in self.claim and self.review before calling this method
            :return: --> entities in the claim and the review in to different variable
        """
        return self.escape(self.get_json_format(self.tagme(claim))), self.escape(self.get_json_format(self.tagme(review)))

    @staticmethod
    def translate_rating_value(initial_rating_value: str) -> str:
        return {
            "True": "TRUE",
            "Misleading": "MIXTURE",
            "False": "FALSE"
        }[initial_rating_value]

    @staticmethod
    def tagme(text) -> list:
        """
            :text:  --> The text in english after translation
            :return:  --> return a list of entities
        """
        if text == "":
            return []
        tagme.GCUBE_TOKEN = VishvasnewsFactCheckingSiteExtractor.TAGME_API_KEY
        return tagme.annotate(text)

    # write this method (and tagme, translate) in an another file cause we can use it in other websites
    @staticmethod
    def get_json_format(tagme_entity):
        '''
            :tagme_entity: must be an object of AnnotateResponse Class returned by tagme function
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
            if tagme_entity.original_json["annotations"][i]["rho"] > min_rho and "dbpedia_categories" in tagme_entity.original_json["annotations"][i]:
                for categorie in tagme_entity.original_json["annotations"][i]["dbpedia_categories"]:
                    entity["categories"].append(categorie)
            i = i + 1
            data_set.append(entity)

        return json.dumps(data_set)

    @staticmethod
    def escape(str):
        str = re.sub('[\n\t\r]', ' ', str)  # removing special char
        str = str.replace('"', '""')  # escaping '"' (CSV format)
        str = re.sub(' {2,}', ' ', str).strip()  # remoing extra spaces
        str = '"' + str + '"'
        return str

    def get_claim_and_print(self, file_name="", err_file_name=""):
        '''
            Extract all claims from vishvasnews and print them to :file_name:
            :file_name: if not spicified write to stdout
            :return:    0 if sucess, -1 if error
        '''
        ERROR = -1
        SUCESS = 0
        LOG = True  # if true print infomation about execution if the script
        extracted = 0  # number of claim exctracted
        not_extracted = 0  # number of claim that the exctraction don't work

        file_name = file_name.strip()  # remove extra spaces
        if file_name != "":
            try:
                file = open(file_name, "w")
            except IOError:
                print("Could not open {}.".format(file_name))
                return ERROR
        else:
            file = sys.stdout
            LOG = False

        err_file_name = err_file_name.strip()
        if err_file_name != "":
            try:
                err_file = open(err_file_name, "w")
            except IOError:
                if LOG:
                    print("Could not open {}.".format(err_file_name))
                err_file = sys.stderr
        else:
            err_file = sys.stderr

        if LOG:
            print("Extracting from vishvasnews.com to {}".format(file_name))
        print("claim_url,claim,review,title, claim_author, links, date, tags, authors, rating_value, claim_entities, review_entities", file=file)

        for retrieve_page in self.retrieve_listing_page_urls():
            if LOG:
                print("Retrieving from : {}".format(retrieve_page))
            parsed_retrieve = self.get(retrieve_page)
            for claim_url in self.retrieve_urls(parsed_retrieve, retrieve_page, 0, self.find_page_count(parsed_retrieve)):
                if LOG:
                    print("Extracting from : {}".format(claim_url))
                webpage = self.get(claim_url)
                if self.is_claim(webpage):
                    extracted += 1
                    claim = self.extract_claim(webpage)
                    review = self.extract_review(webpage)
                    title = self.extract_title(webpage)
                    claimeur = self.extract_claimed_by(webpage)
                    links = self.extract_links(webpage)
                    date = self.extract_date(webpage)
                    tags = self.extract_tags(webpage)
                    authors = self.extract_author(webpage)
                    rating = self.extract_rating_value(webpage)
                    claim_entities, review_entities = self.extract_entities(
                        claim, review)

                    print('{}'.format(claim_url), end=',', file=file)
                    print('{}'.format(claim), end=',', file=file)
                    print('{}'.format(review), end=',', file=file)
                    print('{}'.format(title), end=',', file=file)
                    print('{}'.format(claimeur), end=',', file=file)
                    print('"{}"'.format(str(links)), end=',', file=file)
                    print('{}'.format(date), end=',', file=file)
                    print('"{}"'.format(str(tags)), end=',', file=file)
                    print('"{}"'.format(str(authors)), end=',', file=file)
                    print('{}'.format(rating), end=',', file=file)
                    print('{}'.format(str(claim_entities)), end=',', file=file)
                    print('{}'.format(str(review_entities)), end='\n', file=file)

                else:
                    not_extracted += 1
                    if LOG:
                        print(
                            "Can't extract, the claim from {}".format(claim_url), file=err_file)
        if LOG:
            print("Extraction terminated with sucess.")
            print("{} claim links extracted.".format(extracted+not_extracted))
            print("{} claim extracted.".format(extracted))
            print("{} claim not extracted.".format(not_extracted))
        file.close()
        return SUCESS
