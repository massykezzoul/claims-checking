# -*- coding: utf-8 -*-
import re
from typing import List, Set

from bs4 import BeautifulSoup
from dateparser.search import search_dates
from tqdm import tqdm

from claim_extractor import Claim, Configuration
from claim_extractor.extractors import FactCheckingSiteExtractor, caching

class FatabyyanoFactCheckingSiteExtractor(FactCheckingSiteExtractor):
    
    def __init__(self, configuration: Configuration):
                super().__init__(configuration)

