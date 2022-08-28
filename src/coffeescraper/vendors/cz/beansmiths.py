from vendors.vendors_abstract import *


class _Beansmiths(VendorBase, ABC):
    def product_list(self, soup):
        return soup.select("li.post-item")

    @property
    def base_url(self):
        return "https://beansmiths.com"

    def name(self, list_item):
        return list_item.find("h2", "woocommerce-loop-product__title").text.strip()

    def _eshop_url_getter(self, list_item):
        return list_item.a.attrs["href"]

    def _price_getter(self, list_item) -> str:
        return list_item.find("span", "woocommerce-Price-amount amount").text

    def _price_range(self, price_list, **kwargs) -> int:
        q = 250  # all default prices listed for 250g
        return super()._price_range(price_list[0]/q)

    def photo_url(self, list_item):
        return list_item.a.img.attrs["src"].strip()

    def _keywords_getter(self, list_item):
        return list_item.find("p", "zoznam-chutovy-profil").text.strip().split(", ")

    @scrape_from_product_detail
    def about(self, list_item):
        return list_item.select("div#tab-description")[0].text.strip()


class BeansmithsFilter(_Beansmiths):
    @property
    def download_url(self):
        return "https://beansmiths.com/kategorie-produktu/kava/filtr/"


class BeansmithsEspresso(_Beansmiths):
    @property
    def download_url(self):
        return "https://beansmiths.com/kategorie-produktu/kava/espresso/"