from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import requests
import re


pagination_url = 'https://allo.ua/ua/products/mobile/proizvoditel-xiaomi/'
r = requests.get(pagination_url)
html = bs(r.content, 'html.parser')
paginationEls = html.select('.pagination > ul > li:last-child > a')

total_pages = int((paginationEls[0].contents[0]))

page = 1

products = []

while page <= total_pages:

    url = f'''https://allo.ua/ua/products/mobile/p-{page}/proizvoditel-xiaomi/'''

    r = requests.get(url)
    html = bs(r.content, 'html.parser')
    productEls = html.select('.products-layout__container > .products-layout__item[data-product-id]')

    if len(productEls):
        for productEl in productEls:
            nameEl = productEl.select('.product-card__title')[0]
            name = nameEl.text.strip()
            name = re.sub(r'\([A-Z0-9]+\)', '', name)
            link = nameEl['href']
            price_el = productEl.select('.sum')
            if len(price_el) == 0:
                continue
            price = price_el[0].text
            price = price.replace(" ", "")

            if int(price) is not None and int(price) > 0:
                products.append([name, price, link, url])

    page += 1

df = pd.DataFrame(np.array(products), columns=['name', 'price', 'link', 'url'])
print(df)

df.to_excel('allo.xlsx')