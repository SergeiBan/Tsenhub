import decimal
import io
import math
from datetime import timedelta

import pandas as pd
import requests
from django.apps import apps
from django.utils import timezone
from rest_framework import exceptions, status

from rates.models import Rate


def parse_pricelist(pricelist):
    """Разбирает прайслист поставщика и переименовывает нужные колонки."""
    df = pd.read_csv(
        io.BytesIO(pricelist),
        usecols=['article_', 'netprice_dso'],
        sep=','
    )
    df.sort_values(
        by=['article_', 'netprice_dso'], ascending=False, inplace=True)
    df.drop_duplicates(subset=['article_'], inplace=True)
    df['netprice_dso'] = df['netprice_dso'].replace(
        {',': '.', '#Н/Д': '0'}, regex=True)
    df.rename(
        columns={'article_': 'uid', 'netprice_dso': 'initial_price'},
        inplace=True
    )
    return df.to_dict('records')


def parse_quotes_request(quotes_request_file):
    """
    Из поступившего файла делает список словарей с артикулами и количеством.
    """
    df = pd.read_excel(
        io.BytesIO(quotes_request_file), header=None, dtype={0: str, 1: int})
    df[0] = df[0].replace(
        {' ': '', 'А': 'A', 'Е': 'E', 'С': 'C', 'О': 'O', 'К': 'K', 'М': 'M',
         'Н': 'H', 'Т': 'T', 'В': 'B', 'Х': 'X', 'Р': 'P'},
        regex=True)
    return df.to_dict('records')


CB_URL = 'https://www.cbr-xml-daily.ru/daily_json.js'


def get_rate():
    try:
        response = requests.get(CB_URL).json()
    except Exception:
        raise exceptions.NotFound(
            detail='Курсы валют недоступны',
            code=status.HTTP_417_EXPECTATION_FAILED)
    try:
        rate = response['Valute']['EUR']['Value']
        rate_accurate = decimal.Decimal(str(rate))
        return rate_accurate
    except Exception:
        raise exceptions.NotAcceptable(
            detail='Курс в ответе не обнаружен',
            code=status.HTTP_417_EXPECTATION_FAILED)


def choose_rate(last_rate_db):
    """Выбирает между получением курса евро у ЦБ или из БД."""
    one_day = timedelta(days=1)
    today = timezone.now().today()
    yesterday = today - one_day
    fresh_rate = None

    if not last_rate_db:
        fresh_rate = get_rate()
        Rate.objects.create(currency='EUR', rate=fresh_rate)
        return fresh_rate

    if (
        last_rate_db.date == today and
        last_rate_db.date.hour < 12
        and timezone.now().hour >= 12
    ):
        fresh_rate = get_rate()
        Rate.objects.create(currency='EUR', rate=fresh_rate)

    elif last_rate_db.date == today:
        fresh_rate = last_rate_db.rate

    elif (
        last_rate_db.date == yesterday and
        last_rate_db.date.hour > 12 and
        timezone.now().hour < 12
    ):
        fresh_rate = last_rate_db.rate

    else:
        fresh_rate = get_rate()
        Rate.objects.create(currency='EUR', rate=fresh_rate)

    return fresh_rate


def prepare_quotes(quote_objs, customer):
    """Создает расценки для конкретного пользователя."""
    multiplier = customer.plan.multiplier
    part_model = apps.get_model('parts.Part')
    parts = part_model.objects.filter(uid__in=[obj[0] for obj in quote_objs])
    parts = dict(parts.values_list('uid', 'initial_price'))
    result_parts = []

    last_rate_db = Rate.objects.first()
    fresh_rate = choose_rate(last_rate_db)

    for obj in quote_objs:
        current_price = parts.get(obj[0])
        new_part = {'Артикул': obj[0]}
        if not current_price:
            new_part['Цена за единицу'] = 'отсутствует'
            new_part['Количество'] = 'отсутствует'
            new_part['Итого'] = 'отсутствует'
        else:
            piece_price_rub = current_price * (fresh_rate + 3)
            price_multiplied = math.ceil(piece_price_rub * multiplier)
            if price_multiplied % 10 > 0:
                price_multiplied += (10 - price_multiplied % 10)
            new_part['Цена за единицу'] = price_multiplied
            new_part['Количество'] = obj[1]
            new_part['Итого'] = price_multiplied * obj[1]

        result_parts.append(new_part)

    df = pd.DataFrame.from_dict(result_parts)
    in_memory_output_file = io.BytesIO()
    df.to_excel(in_memory_output_file, sheet_name='Quotes', index=False)
    return in_memory_output_file
