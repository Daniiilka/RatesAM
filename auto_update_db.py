import datetime

import requests
from datetime import datetime

from dotenv import dotenv_values
from peewee import *
from bs4 import BeautifulSoup
config = dotenv_values(".env")

db = PostgresqlDatabase(database='ratesAM', user=config['DB_USER'],
                        password=config['DB_PASSWORD'])


class Rates_Currency(Model):
    rub_usd_uni = FloatField(default=None)
    rub_eur_uni = FloatField(default=None)
    rub_amd_uni = FloatField(default=None)
    usd_amd_sas = FloatField(default=None)
    eur_amd_sas = FloatField(default=None)
    last_update = TimeField(default=None)

    class Meta:
        database = db


def get_data_from_sas():
    usd, eur = 0, 0
    usd_amd_calc = requests.get('https://www.sas.am/en/appfood/personal'
                                '/calculator/')
    soup = BeautifulSoup(usd_amd_calc.text, 'lxml')

    while eur == 0 and usd == 0:
        for line in soup.findAll('div', class_='exchange-table__row'):
            elements = line.findAll('span', class_='exchange-table__cell'
                                                   '-content')
            if elements[0].text == 'USD':
                usd = elements[1].text
            elif elements[0].text == 'EUR':
                eur = elements[1].text

    return usd, eur


def link(currency):
    result = requests.get('https://online.unistream.ru/card2cash/calculate'
                          '?destination=ARM&amount=1000&currency='
                          f'{currency}&accepted_currency=RUB&profile'
                          '=unistream_front')
    result = result.json()
    return result['fees'][0]['rate']


def update_db():
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    data_from_sas = get_data_from_sas()
    usd_amd = data_from_sas[0]
    eur_amd = data_from_sas[1]
    Rates_Currency.create(rub_usd_uni=link('USD'),
                          rub_eur_uni=link('EUR'),
                          rub_amd_uni=link('AMD'),
                          usd_amd_sas=usd_amd,
                          eur_amd_sas=eur_amd,
                          last_update=current_time)



if __name__ == '__main__':
    update_db()
