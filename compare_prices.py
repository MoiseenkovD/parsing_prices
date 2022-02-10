import pandas as pd

allo = pd.read_excel('allo.xlsx', index_col=0)
allo['store'] = 'ALLO'

moyo = pd.read_excel('moyo.xlsx', index_col=0)
moyo['store'] = 'MOYO'

foxtrot = pd.read_excel('foxtrot.xlsx', index_col=0)
foxtrot['store'] = 'FOXTROT'

df = pd.concat([allo, moyo, foxtrot])

duplicated_df = df[df.duplicated(subset=['name'], keep=False)]
sorted_df = duplicated_df.sort_values(by=['name', 'price'], ascending=[True, True])


lowprice_df = sorted_df.groupby('name').first()
lowprice_df.to_excel('low-price.xlsx')


other_df = sorted_df.groupby('name').apply(lambda group: group.iloc[1:, 1:])
other_df.to_excel('other_prices.xlsx')


