from vendors.vendors_abstract import *


class _PoppyBeans(VendorBase, ABC):
    def product_list(self, soup):
        return soup.select(".card")

    @property
    def base_url(self):
        return "https://poppybeans.cz/"

    def name(self, list_item):
        return list_item.find("h3", {"class": "card__name"}).text.strip()

    def _eshop_url_getter(self, list_item):
        return urllib.parse.urljoin(self.base_url, list_item.a.attrs['href'])

    def _price_getter(self, list_item) -> str:
        return list_item.find("div", {"class": "card__price"}).text.strip().replace("Od ", "")

    def _price_range(self, price_list, **kwargs) -> int:
        q = 250  # all default prices listed for 250g
        return super()._price_range(price_list[0]/q)

    def photo_url(self, list_item):
        return "https:" + list_item.find("div", {"class": "card__image-wrapper"}).img.attrs["src"]

    @scrape_from_product_detail
    def _keywords_getter(self, list_item):
        return list_item.find("h4").text.split(", ")

    @scrape_from_product_detail
    def about(self, list_item):
        return list_item.select("div .rte > p")[-1].text.strip()


class PoppyBeansFilter(_PoppyBeans):
    @property
    def download_url(self):
        return "https://poppybeans.cz/collections/zrnkova-kava/filter"


class PoppyBeansEspresso(_PoppyBeans):
    @property
    def download_url(self):
        return "https://poppybeans.cz/collections/zrnkova-kava/espresso"