from vendors.vendors_abstract import *


class _Chroast(VendorBase, ABC):
    def product_list(self, soup):
        return soup.select("div.product")

    @property
    def base_url(self):
        return "https://www.chroast.cz/"

    def name(self, list_item):
        return list_item.find("a", "name").text.strip().capitalize()

    def _eshop_url_getter(self, list_item):
        return urllib.parse.urljoin(self.base_url, list_item.find("a", "name").attrs["href"])

    @scrape_from_product_detail
    def _price_getter(self, list_item) -> str:
        return list_item.find("span", "price-final-holder").text

    @scrape_from_product_detail
    def _get_quantity(self, list_item) -> int:
        tmp = list_item.find_all("option")[-1].text.strip()  # cheapest always last (as seen so far)
        tmp = tmp[:tmp.index("g")]
        return int(tmp)

    def _price_range(self, price_list, **kwargs) -> int:
        q = self._get_quantity(kwargs["list_item"])
        return super()._price_range(price_list[0]/q)

    def photo_url(self, list_item):
        return list_item.a.img.attrs["src"].strip()

    @scrape_from_product_detail
    def _keywords_getter(self, list_item):
        return list_item.select(".p-short-description > p")[0].text.strip().split("|")


class ChroastFilter(_Chroast):
    @property
    def download_url(self):
        return "https://www.chroast.cz/filtr/"


class ChroastEspresso(_Chroast):
    @property
    def download_url(self):
        return "https://www.chroast.cz/espresso/"