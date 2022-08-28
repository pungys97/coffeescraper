from vendors.vendors_abstract import *


class _Doubleshot(VendorBase, ABC):
    def product_list(self, soup):
        return soup.select(".productGrid-product")

    @property
    def base_url(self):
        return "https://www.doubleshot.cz/"

    def name(self, list_item):
        return list_item.find("div", "productBox loadPanel").attrs.get("title", None)

    def _eshop_url_getter(self, list_item):
        return urllib.parse.urljoin(self.base_url, list_item.find("a", "productBox-link").attrs.get('href', ""))

    def _price_getter(self, list_item) -> str:
        return list_item.find("div", "productBox-price").text

    @scrape_from_product_detail
    def _get_quantity(self, list_item) -> int:
        return int(list_item.find("span", "productDetail-stat").text.replace("g", "").strip())

    def _price_range(self, price_list, **kwargs) -> int:
        try:
            q = self._get_quantity(kwargs['list_item'])
        except AttributeError:
            q = 350 # most values are 350
        return super()._price_range(price_list[0]/q)

    def photo_url(self, list_item):
        return list_item.img.attrs['src'].strip()

    def _keywords_getter(self, list_item):
        return list_item.find("div", "productBox-taste").contents[0].split(",")

    @scrape_from_product_detail
    def about(self, list_item):
        return list_item.find("p", {"class": "productDetail-description"}).text.strip()


class DoubleshotFilter(_Doubleshot):
    @property
    def download_url(self):
        return "https://www.doubleshot.cz/cs/taxons/filtrovana-kava"


class DoubleshotEspresso(_Doubleshot):
    @property
    def download_url(self):
        return "https://www.doubleshot.cz/cs/taxons/espresso"