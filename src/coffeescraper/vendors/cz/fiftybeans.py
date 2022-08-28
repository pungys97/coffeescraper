from vendors.vendors_abstract import *


class _FiftyBeans(VendorBase, ABC):
    def product_list(self, soup):
        return soup.select("article.product-miniature")

    @property
    def base_url(self):
        return "https://fiftybeans.cz/"

    def name(self, list_item):
        return list_item.h3.text.strip()

    def _eshop_url_getter(self, list_item):
        return list_item.a.attrs["href"]

    def _price_getter(self, list_item) -> str:
        return " ".join(list_item.find("span", "price").text.split())

    def _price_range(self, price_list, **kwargs) -> int:
        q = 200  # all default prices listed for 250g
        return super()._price_range(price_list[0]/q)

    def photo_url(self, list_item):
        return list_item.a.img.attrs["src"].replace("594-large_default", "595-home_default")

    def _keywords_getter(self, list_item):
        return []


class FiftyBeansFilter(_FiftyBeans):
    @property
    def download_url(self):
        return "https://fiftybeans.cz/cs/11-vyberova-kava?q=Kategorie-Káva+na+filtr"


class FiftyBeansEspresso(_FiftyBeans):
    @property
    def download_url(self):
        return "https://fiftybeans.cz/cs/11-vyberova-kava?q=Kategorie-Káva+na+espresso"