from vendors.vendors_abstract import *


class FathersCoffee(VendorBase, ABC):
    def product_list(self, soup):
        return soup.select("div.product-item")

    @property
    def download_url(self):
        return self.base_url

    @property
    def base_url(self):
        return "https://fatherscoffee.cz"

    def name(self, list_item):
        return list_item.a.attrs["title"]

    def _eshop_url_getter(self, list_item):
        return list_item.a.attrs['href']

    @scrape_from_product_detail
    def _price_getter(self, list_item) -> str:
        return list_item.find("p", "price").text.split(" - ")[0]

    def _price_range(self, price_list, **kwargs) -> int:
        """
        Doubleshot is expensive --> classify all as expensive
        :param **kwargs:
        :param price_list:
        :return:
        """
        q = 300 # default == 300g, could mess up price range but not currently important
        return super()._price_range(price_list[0]/q)

    def photo_url(self, list_item):
        return list_item.a.img.attrs["data-lazy-src"].strip()

    @scrape_from_product_detail
    def _keywords_getter(self, list_item):
        tmp = list_item.select("div.woocommerce-product-details__short-description p")
        keywords = []
        for p in tmp:
            if "Chuťový profil:" in p.text:
                try:
                    keywords = p.contents[-1].split(", ")
                except TypeError:
                    keywords = p.text.replace("Chuťový profil:", "").split(", ")
                break
        return keywords

    @scrape_from_product_detail
    def about(self, list_item):
        return list_item.select("div.woocommerce-product-details__short-description > p")[-1].text.strip()

    def brewing_methods(self, list_item):
        try:
            tags = list_item.find("div", "berocket_better_labels_position").text
        except AttributeError:
            return []
        if self._espresso in tags.lower():
            return self._espresso
        return self._filter
