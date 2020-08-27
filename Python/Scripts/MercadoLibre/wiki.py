import requests, bs4, webbrowser, sys

#! Python 3

"""
    Searches for all relevant announcenments of a given product
"""

#4/7/2020
SAMPLES = 3
BROWSER = 'C:\Program Files\Mozilla Firefox'


class Searcher():
    def __init__(self, *args):
        self.url = "https://listado.mercadolibre.com.co/" 
        self.seller_level = "green"
        self.digest_args(args)

    def digest_args(self, args):
        """ concatenate each arg 
            args:
                seller_level + color
                price  - find cheapests products
        
        """
        low_price = False
        reading_args = False
        boundary = 0
        keywords = []
        for index,arg in enumerate(args):
            if arg == 'seller_level':
                self.seller_level = args[index + 1]
                reading_args = True
                boundary = index
            elif arg.startswith('price'):
                reading_args = True
                low_price = True
            if not reading_args:
                keywords.append(arg)

        product = "-".join( keywords ) #fast concatenation
        self.search(product, low_price=low_price)
    
    def get_page(self, url):
        """ save some code from writing the same everytime"""
        try:
            page = requests.get(url)
            page.raise_for_status()#check response
            return page
        except requests.exceptions.HTTPError as e:
            print(f"[ERROR] Page didn't get it. -{e}-.")
            return
    
    def search(self, product, low_price = True):
        """ """
        url = self.url + product   
        url_headers = []
        if low_price:
            url += "_OrderId_PRICE"
        page = self.get_page(url)

        soup = bs4.BeautifulSoup(page.text, "html.parser")
        css_selector = "li.ui-search-layout__item"
        headers = soup.select(css_selector)
        if not headers:
            print(f"[INFO] No articles matched {product}") 
            return
        for header in headers:
            url = self.get_header_link(header)
            seller_page = self.get_page(url)
            if not self.check_reputation(url, seller_page):
                continue
            url_headers.append(url)
            if len(url_headers) == SAMPLES:
                break
        if not url_headers:
            print(f"[INFO] {self.seller_level} were matched.")
        else:
            for url in url_headers:
                self.open_seller_page(url)

    
    def open_seller_page(self, url):
        # browser = webbrowser.Mozilla('mozilla')

        webbrowser.open_new_tab(url)
        #TODO: save url, and implement limit of pages

    
    def get_header_link(self, header):
        """ find link from soup object"""
        a_set = header.findChildren("a", recursive=True)
        if not a_set:
            return
        for element in a_set:
            class_name = " ".join(element['class'])
            if class_name.startswith('ui-search'):
                target_element = element
                break
        if not target_element:
            return
        url = target_element["href"]
        return url

    def check_reputation(self, url, page):
        """ dissect seller state, and catalogize them as goood or not"""
        seller_soup = bs4.BeautifulSoup(page.text, "html.parser")
        seller_info = seller_soup.select("div.reputation")[0]
        bar_title = " ".join(seller_info.get("class")) #check later
        if not self.seller_level in bar_title:
            return False
        else:
            return True


if __name__ == "__main__":
    Searcher(*sys.argv[1:])

