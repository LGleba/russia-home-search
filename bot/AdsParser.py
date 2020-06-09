import requests
from math import ceil

# Parser

class Ad:
    def __init__(self, **kwargs):
        self.url = kwargs.get('url', '') # ссылка
        self.title = kwargs.get('title', '') # название
        self.address = kwargs.get('address', '') # адрес
        self.price = kwargs.get('price', '') # цена

class Parser:
    def __init__(self, **kwargs):
        self.city = kwargs.get('city', 'moskva') # город
        self.buy = kwargs.get('buy', 'kupit') # 'kupit'/'snyat'
        self.house_type = kwargs.get('home', 'kvartira') # 'kvartira'/'dom'
        self.price_min = kwargs.get('price_min', '') # минимальная цена
        self.price_max = kwargs.get('price_max', '') # максимальная цена
        self.metro = kwargs.get('metro', '') # метро
        
        self.pages = []
        self.index = 0
        
    def configure(self, **kwargs):
        if 'city' in kwargs: 
            self.city = kwargs.get('city') # город
            if not self.city:
                self.city = 'moskva'
                
        if 'buy' in kwargs:
            self.buy = kwargs.get('buy') # 'kupit'/'snyat'
            if not self.buy:
                self.buy = 'kupit'
                
        if 'home' in kwargs:
            self.house_type = kwargs.get('home') # 'kvartira'/'dom'
            if not self.house_type:
                self.house_type = 'kvartira'
                
        if 'price_min' in kwargs:
            self.price_min = kwargs.get('price_min') # минимальная цена
        if 'price_max' in kwargs:
            self.price_max = kwargs.get('price_max') # максимальная цена
        if 'metro' in kwargs:
            self.metro = kwargs.get('metro') # метро

    def translit(self, s):
        letters = {'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'e',
          'ж':'zh','з':'z','и':'i','й':'i','к':'k','л':'l','м':'m','н':'n',
          'о':'o','п':'p','р':'r','с':'s','т':'t','у':'u','ф':'f','х':'h',
          'ц':'c','ч':'cz','ш':'sh','щ':'sch','ъ':'','ы':'y','ь':'','э':'e',
          'ю':'yu','я':'ya', ' ':'-'}

        s = s.lower()
        for key in letters:
            s = s.replace(key, letters[key])

        return s

    def form_request_yandex(self):
        url = 'https://realty.yandex.ru/'

        if self.city:
            url += self.translit(self.city) + '/'
        if self.buy:
            url += self.translit(self.buy) + '/'
        if self.house_type:
            url += self.translit(self.house_type) + '/'
            
        if self.metro:
            url += 'metro-' + self.translit(self.metro) + '/'
        
        if self.price_min or self.price_max:
            url += '?'

        if self.price_min:
            url += '&priceMin=' + self.price_min
        if self.price_max:
            url += '&priceMax=' + self.price_max

        return url
    
    def page_init_yandex(self, nmax):
        url = self.form_request_yandex()
        
        page = 0
        response = requests.get(url + '&page=' + str(page))
        while response and page < ceil(nmax / 24.0):
            # bytes; encoding == latin-1
            self.pages.append(response.content)
            page += 1;
            response = requests.get(url + '&page=' + str(page))

        self.index = 0

    def get_ad_yandex(self, index):
        page = index // 24
        if page > len(self.pages) - 1:
            return None
        
        while self.index < index:
            pos = self.pages[page].find('href="/offer/'.encode('latin-1'))
            if pos == -1:
                print(self.index)
                return None
            self.pages[page] = self.pages[page][pos + 6:]
            self.index += 1
                
        # url
        pos = self.pages[page].find('href="/offer/'.encode('latin-1'))
        if pos == -1:
            return None
        self.pages[page] = self.pages[page][pos + 6:]
        ref = 'https://realty.yandex.ru' + self.pages[page][:self.pages[page]
                                        .find('"'.encode('latin-1'))].decode() 

        # title
        pos = self.pages[page].find('OffersSerpItem__title'.encode('latin-1'))
        self.pages[page] = self.pages[page][pos + 23:]
        title = self.pages[page][:self.pages[page].find('<'.encode('latin-1'))].decode()

        # address
        pos = self.pages[page].find('OffersSerpItem__address'.encode('latin-1'))
        self.pages[page] = self.pages[page][pos + 25:]
        address = self.pages[page][:self.pages[page].find('<'.encode('latin-1'))].decode()

        # price
        pos = self.pages[page].find('OffersSerpItem__price'.encode('latin-1'))
        self.pages[page] = self.pages[page][pos + 43:]
        price = self.pages[page][:self.pages[page].find('<'.encode('latin-1'))].decode()
                
        return Ad(url=ref, title=title, address=address, price=price)
