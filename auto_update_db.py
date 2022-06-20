import datetime

import psycopg2

import requests
from datetime import datetime

from dotenv import dotenv_values
from bs4 import BeautifulSoup


config = dotenv_values(".env")


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
    data_from_sas = get_data_from_sas()
    usd_amd = data_from_sas[0]
    eur_amd = data_from_sas[1]
    conn = psycopg2.connect(dbname='ratesAM', user=config['DB_USER'],
                            password=config['DB_PASSWORD'],
                            host=config['DB_HOST'],
                            )
    cursor = conn.cursor()
    cursor.execute('INSERT INTO rates_currency (rub_usd_uni, rub_eur_uni, '
                   'rub_amd_uni, usd_amd_sas, eur_amd_sas, last_update) '
                   'VALUES (%s, %s, %s, %s, %s, %s)', (link('USD'),
                                                       link('EUR'),link('AMD'),
                                                       usd_amd, eur_amd, datetime.now()))
    conn.commit()
    cursor.close()
    conn.close()


if __name__ == '__main__':
    update_db()
