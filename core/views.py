from io import BytesIO
import pandas as pd


def parse_pricelist(pricelist):
    pricelist = BytesIO(pricelist.read())

    df = pd.read_csv(pricelist, usecols=['article_', 'description', 'netprice_dso'], sep=',', decimal=',')
    df['description'] = df['description'].astype('category')

    return df.to_dict('records')



    

