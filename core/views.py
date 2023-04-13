import io
import pandas as pd
from django.apps import apps



def parse_pricelist(pricelist):
    df = pd.read_csv(io.BytesIO(pricelist), usecols=['article_', 'netprice_dso'], sep=',', decimal=',')
    df.sort_values(by=['article_', 'netprice_dso'], ascending=False, inplace=True)
    df.drop_duplicates(subset=['article_'], inplace=True)
    df.rename(columns={'article_': 'uid', 'netprice_dso': 'initial_price'}, inplace=True)
    return df.to_dict('records')


def parse_quotes_request(quotes_request_file):
    """
    Из поступившего файла делает список словарей с артикулами и количеством.
    """
    df = pd.read_excel(io.BytesIO(quotes_request_file), header=None)
    return df.to_dict('records')

def prepare_quotes(quote_objs):
    Part = apps.get_model('parts.Part')
    parts = Part.objects.filter(uid__in=[obj[0] for obj in quote_objs])
    parts = parts.values_list('uid', 'initial_price')
    df = pd.DataFrame.from_dict(parts)
    print(df)
    in_memory_output_file = io.BytesIO()
    df.to_excel(in_memory_output_file, sheet_name='Quotes', index=False)
    return in_memory_output_file
    

