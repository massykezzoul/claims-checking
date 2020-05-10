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
from yandex_translate import YandexTranslateException

import json
import math
import tagme

sys.path.append("../tagme")


class FatabyyanoFactCheckingSiteExtractor:
    # Constants
    YANDEX_API_KEY = 'trnsl.1.1.20200311T210815Z.796b747ff14857c9.2e7b856527d2689a26379ff56769f5b3c087f55b'
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

    def retrieve_urls(self, parsed_claim_review_page: BeautifulSoup, listing_page_url: str, number_of_pages: int) -> List[str]:
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
        json_claim, json_body = self.extract_entities(self.claim, self.review)
        claim.set_claim_entities(json_claim)
        claim.set_body_entities(json_body)

        return [claim]

    def is_claim(self, parsed_claim_review_page: BeautifulSoup) -> bool:
        return True

    def extract_claim(self, parsed_claim_review_page: BeautifulSoup) -> str:
        claim = parsed_claim_review_page.select_one("h1.post_title")
        if claim:
            return self.escape(claim.text)
        else:
            # print("something wrong in extracting claim")
            return ""

    def extract_review(self, parsed_claim_review_page: BeautifulSoup) -> str:
        return self.escape(parsed_claim_review_page.select_one(
            "section.l-section.wpb_row.height_small div[itemprop=\"text\"]").text)

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

    def extract_entities(self, claim, review):
        """
            You should call extract_claim and extract_review method and
            store the result in self.claim and self.review before calling this method
            :return: --> entities in the claim and the review in to different variable
        """
        return self.escape(self.get_json_format(self.tagme(self.translate(claim)))), self.escape(self.get_json_format(self.tagme(self.translate(review))))

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
    def translate(text: str) -> str:
        """
            :text:  --> The text in arabic
            :return:  --> return a translation of :text: in english
        """
        DEBUG = False

        if text == "":
            return ""
        self = FatabyyanoFactCheckingSiteExtractor
        yandexAPI = self.YANDEX_API_KEY
        yandex = YandexTranslate(yandexAPI)

        responses = []
        try:
            response = yandex.translate(text, 'ar-en')
            if DEBUG:
                print("response : " + response, end='\n\n')
            responses = [response]
            text_too_long = False
        except YandexTranslateException as e:
            if e.args == 'ERR_TEXT_TOO_LONG' or 'ERR_TEXT_TOO_LONG' in e.args:
                text_too_long = True
            else:
                print(text, end='\n\n')
                print("Erreur API Yandex\nCode d'erreur : " + str(e.args))
                sys.exit(1)

        text_list = [text]

        while text_too_long:
            if DEBUG:
                print("cutting : " + str(text_list), end='\n\n')
            text_too_long = False
            try:
                text_list = self.cut_str(text_list)
            except ValueError:
                print("Erreur ")
                sys.exit(1)
            responses = []
            for t in text_list:
                try:
                    responses.append(yandex.translate(t, 'ar-en'))
                except YandexTranslateException:
                    text_too_long = True
                    continue

        text_list = []
        for r in responses:
            if int(r['code'] != 200):
                print(
                    "Erreur lors de la traduction\nCode de l'erreur : " + r['code'])
                sys.exit(1)
            else:
                text_list.append(r['text'][0])

        return self.concat_str(text_list)

    @staticmethod
    def tagme(text):
        """
            :text:  --> The text in english after translation
            :return:  --> return a list of entities
        """
        if text == "":
            return []
        tagme.GCUBE_TOKEN = FatabyyanoFactCheckingSiteExtractor.TAGME_API_KEY
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
            if tagme_entity.original_json["annotations"][i]["rho"] > min_rho and "dbpedia_categories" in tagme_entity.original_json["annotations"][i]:
                for categorie in tagme_entity.original_json["annotations"][i]["dbpedia_categories"]:
                    entity["categories"].append(categorie)
            i = i + 1
            data_set.append(entity)

        return json.dumps(data_set)

    @staticmethod
    def cut_str(str_list):
        # cut string
        result_list = []

        for string in str_list:
            middle = math.floor(len(string) / 2)
            before = string.rindex(' ', 0, middle)
            after = string.index(' ', middle + 1)

            if middle - before < after - middle:
                middle = before
            else:
                middle = after

            result_list.append(string[:middle])
            result_list.append(string[middle + 1:])

        return result_list

    @staticmethod
    def concat_str(str_list):
        result = ""

        for string in str_list:
            result = result + ' ' + string

        return result[1:]

    @staticmethod
    def escape(str):
        str = re.sub('[\n\t\r]', ' ', str)  # removing special char
        str = str.replace('"', '""')  # escaping '"' (CSV format)
        str = re.sub(' {2,}', ' ', str).strip()  # remoing extra spaces
        str = '"' + str + '"'
        return str

    def get_claim_and_print(self, file_name="", err_file_name=""):
        '''
            Extract all claims from fatabyyano and print them to :file_name:
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
            print("Extracting from fatabyyano.com to {}".format(file_name))
        print("claim_url,claim, title, claim_author, links, date, tags, authors, rating_value, claim_entities, review_entites", file=file)

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
                    title = claim  # self.extract_title(webpage)
                    claimeur = ""  # self.extract_claimed_by(webpage)
                    links = self.extract_links(webpage)
                    date = self.extract_date(webpage)
                    tags = self.extract_tags(webpage)
                    authors = self.extract_author(webpage)
                    rating = self.extract_rating_value(webpage)
                    claim_entities, review_entities = self.extract_entities(
                        claim, review)

                    print('"{}"'.format(claim_url), end=',', file=file)
                    print('{}'.format(claim), end=',', file=file)
                    print('{}'.format(title), end=',', file=file)
                    print('"{}"'.format(claimeur), end=',', file=file)
                    print('"{}"'.format(str(links)), end=',', file=file)
                    print('{}'.format(date), end=',', file=file)
                    print('"{}"'.format(str(tags)), end=',', file=file)
                    print('{}'.format(str(authors)), end=',', file=file)
                    print('{}'.format(rating), end=',', file=file)
                    print('{}'.format(str(claim_entities)),
                          end=',', file=file)
                    print('{}'.format(str(review_entities)),
                          end='\n', file=file)
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
