from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import requests
import re

pagination_url = 'https://www.foxtrot.com.ua/uk/shop/mobilnye_telefony_xiaomi.html'
r = requests.get(pagination_url)
html = bs(r.content, 'html.parser')
paginationEls = html.select('.listing__pagination > ul > li')

total_pages = int(paginationEls[-2]['data-page'])

page = 1

products = []

while page <= total_pages:

    url = 'https://www.foxtrot.com.ua/uk/shop/mobilnye_telefony_xiaomi.html?page=' + str(page)

    r = requests.get(url)
    html = bs(r.content, 'html.parser')
    phoneEls = html.select('.listing__body-wrap .card.js-card.sc-product')

    if len(phoneEls):
        for phoneEl in phoneEls:
            link = phoneEl['data-url']
            cardEl = phoneEl.select('.card__head')
            card = cardEl[0]
            name = card.attrs['data-title'].strip().replace('Смартфон ', '')
            name = re.sub(r'\([A-Z0-9]+\)', '', name)
            price = card.attrs['data-price']

            if int(price) is not None and int(price) > 1:
                products.append([name, price, link, url])

    page += 1

df = pd.DataFrame(np.array(products), columns=['name', 'price', 'link', 'url'])
print(df)

df.to_excel('foxtrot.xlsx')

