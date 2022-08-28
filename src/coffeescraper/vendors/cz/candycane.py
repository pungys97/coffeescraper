from vendors.vendors_abstract import *


class _CandyCane(VendorBase, ABC):
    def product_list(self, soup):
        return soup.select("li.product")

    @property
    def base_url(self):
        return "https://www.candycane.coffee"

    def name(self, list_item):
        return list_item.find("h2", "product__title").text.strip()

    def _eshop_url_getter(self, list_item):
        return list_item.a.attrs["href"]

    def _price_getter(self, list_item) -> str:
        return list_item.find("input", {"name": "gtm4wp_price"}).attrs["value"] + " Kč"

    def _get_quantity(self, list_item) -> int:
        return int(list_item.find("option", selected=True).text.replace("k", "").replace("g", "").strip())

    def _price_range(self, price_list, **kwargs) -> int:
        try:
            q = self._get_quantity(kwargs['list_item'])
        except AttributeError:
            q = 250 # most values are 250g
        return super()._price_range(price_list[0]/q)

    def photo_url(self, list_item):
        return list_item.img.attrs['src']

    def _keywords_getter(self, list_item):
        return list_item.find("p", "product__short-description").text.split(",")


class CandyCaneFilter(_CandyCane):
    @property
    def download_url(self):
        return "https://www.candycane.coffee/obchod/?_categories=kava&_roasting=filtr"


class CandyCaneEspresso(_CandyCane):
    @property
    def download_url(self):
        return "https://www.candycane.coffee/obchod/?_categories=kava&_roasting=espresso"
