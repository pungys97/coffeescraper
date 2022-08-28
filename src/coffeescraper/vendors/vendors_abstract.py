import inspect
import logging
from abc import ABC, abstractmethod
from typing import Optional, Union
import urllib.parse  # keep it here used in subclasses

from bs4 import BeautifulSoup
from icecream import ic
from price_parser import Price

from constants.coffee_predefined_settings import upper_bound_for_price_0, upper_bound_for_price_1, SKIP_THESE_NAMES
from data_fetching.fetch import fetch_text
from settings import logging_level

logging.getLogger().setLevel(logging_level)


def to_file(obj, f: str = "dummy.pkl"):
    with open(f, "wb") as fp:
        import pickle
        import sys
        sys.setrecursionlimit(30000)
        pickle.dump(obj, fp)


def parse_price(price: str) -> list:
    parsed_price = Price.fromstring(price)
    ret = [
        parsed_price.amount_float,
        parsed_price.currency
    ]
    return ret


def scrape_from_product_detail(function):
    """
    Annotate vendor methods that need to fetch coffee details.
    :param obj: self
    :return:
    """

    sig = inspect.signature(function)
    assert sig.parameters.get("list_item", False), "scrape_from_product_detail can only " \
                                                   "be applied to methods that take " \
                                                   "list_item as argument "
    idx_list_item = list(sig.parameters.keys()).index("list_item")

    def wrapper(*args, **kwargs):
        obj = args[0]  # self
        url = obj.__dict__.get("_url_to_current_product", None)
        soup = obj.__dict__.get("_soup_of_current_product", None)
        if soup is None:
            fetched_text = fetch_text(url)
            soup = BeautifulSoup(fetched_text, 'html.parser')
            obj._soup_of_current_product = soup
        args = (arg if idx != idx_list_item else soup for idx, arg in enumerate(args))  # replace list_item with soup object
        result = function(*args, **kwargs)
        return result

    return wrapper


class VendorBase(ABC):
    _filter = "filter"
    _espresso = "espresso"
    _skip_these_names = SKIP_THESE_NAMES
    _url_to_current_product = None
    _soup_of_current_product = None

    def __init__(self):
        self._keywords = []

    def __str__(self):
        return self.download_url

    @property
    @abstractmethod
    def download_url(self) -> str:
        """
        Url pointing to the list of products. Can contain {start} and {offset} keywords
        which will be replaced at evaluation. Useful for long list (1000x) --> scraping
        can run in parallel.
        :return: URL (string)
        """
        pass

    @property
    @abstractmethod
    def base_url(self) -> str:
        """
        Url used as base. Product details usually only contain relative reference.
        :return: URL (string)
        """
        pass

    @abstractmethod
    def product_list(self, soup):
        """
        Get iterable of product items to iterate over and scrape contents.
        :param soup: Beautiful soup object containing fetched content.
        :return: iterable of bs object representing items.
        """
        pass

    @abstractmethod
    def name(self, list_item) -> Optional[str]:
        pass

    def eshop_url(self, list_item):
        self._soup_of_current_product = None # always discard current soup in url changes
        self._url_to_current_product = self._eshop_url_getter(list_item)
        return self._url_to_current_product

    @abstractmethod
    def _eshop_url_getter(self, list_item) -> Optional[str]:
        pass

    @abstractmethod
    def _price_getter(self, list_item) -> str:
        """
        Should extract price in format xxx yy where xxx is value and yy is currency.
        :param list_item: bs soup object from where to extract the value
        :return: string xxx yy (100 Kč)
        """
        pass

    @property
    def acidity(self) -> int:
        return 0

    @property
    def sweetness(self) -> int:
        return 0

    @property
    def bitterness(self) -> int:
        return 0

    def _price_range(self, price, price_thresholds=(upper_bound_for_price_0, upper_bound_for_price_1), **kwargs) -> int:
        """
        Returns whether the coffee is affordable, medium, expensive.
            0 price < price_thresholds[0] Kč/g
            1 price_thresholds[0] < price < price_thresholds[1]
            2 > price_thresholds[1]
        :param price: kc/kg
        :return: int [0,1,2]
        """
        if price < price_thresholds[0]:
            return 0
        elif price < price_thresholds[1]:
            return 1
        else:
            return 2

    def price(self, list_item) -> Union[tuple[list, int], tuple[None, None]]:
        """
        Returns price as a list [amount, currency] and price_range [0,1,2] -> 0 affordable x 2 expensive
        :param list_item:
        :return:
        """
        _price = self._price_getter(list_item)
        if _price:
            _price = parse_price(_price)
            return _price, self._price_range(_price, list_item=list_item)
        else:
            return None, None

    @abstractmethod
    def photo_url(self, list_item) -> Optional[str]:
        pass

    @abstractmethod
    def _keywords_getter(self, list_item) -> Optional[list]:
        pass

    def keywords(self, list_item) -> Optional[list]:
        self._keywords = self._keywords_getter(list_item)
        return [w.strip().capitalize() for w in self._keywords]

    def about(self, list_item) -> Optional[str]:
        """
        Returns about paragraph, if not implemented in subclass, returns default texting.
        :param list_item:
        :return: (espresso, filter) one of
        """
        return "Tato káva nemá popis dostupný."

    def roast_level(self, list_item) -> str:
        return ""

    def brewing_methods(self, *args) -> list[str]:
        """
        Returns brewing method, not a property because some roasters have separate pages
        for different methods other have it as attribute.
        :param list_item:
        :return: (espresso, filter) one of
        """
        if self._filter in self.__class__.__name__.lower():
            return [self._filter]
        elif self._espresso in self.__class__.__name__.lower():
            return [self._espresso]
        else:
            return []

    @property
    def skip_these_names(self):
        return self._skip_these_names
