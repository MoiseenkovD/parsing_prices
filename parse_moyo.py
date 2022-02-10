from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import requests
import re

pagination_url = 'https://www.moyo.ua/ua/telecommunication/smart/xiaomi/'
r = requests.get(pagination_url)
html = bs(r.content, 'html.parser')
paginationEls = html.select('.load-section_pagination > ul > li:last-child > a')

total_pages = (paginationEls[0].contents[0])

page = 1

products = []

while page <= int(total_pages):

        url = f'''https://www.moyo.ua/ua/telecommunication/smart/xiaomi/?page={page}'''
        r = requests.get(url)
        html = bs(r.content, 'html.parser')

        phoneEls = html.select('.catalog_products > .product-item')
        if len(phoneEls):
            for phoneEl in phoneEls:
                name = phoneEl['data-name'].strip().replace('Смартфон ', '')
                name = re.sub(r'\([A-Z0-9]+\)', '', name)
                price = phoneEl['data-price']
                link = phoneEl.contents[1]['href']

                if int(price) is not None and int(price) > 0:
                    products.append([name, price, link, url])

        page += 1

df = pd.DataFrame(np.array(products), columns=['name', 'price', 'link', 'url'])
print(df)

df.to_excel('moyo.xlsx')
