import pickle
import sys
from functools import cache

from vendors.vendors_abstract import *


class DosMundos(VendorBase, ABC):
    def product_list(self, soup):
        return soup.select(".product")

    @property
    def download_url(self):
        return "https://www.dos-mundos.cz/jednodruhova-kava-100--arabica/"

    @property
    def base_url(self):
        return "https://www.dos-mundos.cz/"

    def name(self, list_item):
        return list_item.find("a", "name").text.strip()

    def _eshop_url_getter(self, list_item):
        return urllib.parse.urljoin(self.base_url, list_item.a.attrs['href'])

    def _price_getter(self, list_item) -> str:
        return list_item.find("div", "price price-final").text.strip().replace("od ", "")  # starts with "od"

    def photo_url(self, list_item):
        return list_item.img.attrs['data-src'].strip()

    def _price_range(self, price_list, **kwargs) -> int:
        """
        Francin has prices for 250g --> kc/g == price_list[0] / 250
        :param **kwargs:
        :param price_list:
        :return:
        """
        return 2

    @scrape_from_product_detail
    def _keywords_getter(self, list_item):
        tmp = list_item.find_all("p")
        keywords = []
        for p in tmp:
            txt = p.text
            if any(word in txt for word in ["Chuťový profil:", "Charakteristika kávy:"]):
                keywords = p.contents[1].split(", ")
                break
        return keywords

    def brewing_methods(self, list_item):
        try:
            tags = list_item.find("div", "flags").text
        except AttributeError:
            tags = ""
        if self._espresso in tags.lower():
            return self._espresso
        return self._filter
