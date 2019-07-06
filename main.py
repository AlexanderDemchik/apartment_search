import urllib.request
from pyquery import PyQuery as pq
from Apartment import Apartment
from Database import Database
import time
import logging
import dateutil.parser
from VkApi import VkApi
from datetime import datetime, timedelta

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logging.info("Started")

db = Database()
vk_api = VkApi()

cookieProcessor = urllib.request.HTTPCookieProcessor()
opener = urllib.request.build_opener(cookieProcessor)
opener.addheaders = [
    ('User-agent',
     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'),
    ('Accept-Language', 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'),
]


def convert_to_iso_date(dt):
    splitted = dt.split(',')
    time = splitted[0]
    date = splitted[1]
    splitted = date.lstrip().split('.')
    return splitted[2] + '-' + splitted[1] + '-' + splitted[0] + ' ' + time + ':00.000'

def convert_iso_date_to_python_date(iso_date):
    return dateutil.parser.parse(iso_date)

def get_apartments_from_page(page):
    apartments = []
    response = opener.open(
        'http://brest.irr.by/realestate/longtime/search/rooms=2%2C3/price=%D0%BE%D1%82+100+%D0%B4%D0%BE+400/currency=BYN/list=list/page{}/'.format(
            page))
    html = response.read().decode('utf-8')
    page = pq(html)

    list_of_apartments = page.find('.add_list')

    for i in range(list_of_apartments.length):
        apartments.append(Apartment(list_of_apartments.eq(i).find(".add_title").attr('href'),
                                    list_of_apartments.eq(i).find('.add_cost').text(),
                                    list_of_apartments.eq(i).find(".add_title").text(),
                                    convert_to_iso_date(list_of_apartments.eq(i).find(".add_data").text())))
    return apartments


def format_apartment_message(apartment):
    return 'Title: ' + apartment.title + '\n' + 'Cost: ' + apartment.price + '\n' + 'Date: ' + apartment.date + '\n' + 'Link: ' + apartment.link


while True:
    try:
        stop_date = datetime.now() - timedelta(days=7)
        apartments = db.fetch()
        fetched_apartments = []
        apartments_to_be_saved = []

        for i in range(3):
            fetched_apartments = fetched_apartments + get_apartments_from_page(i)

        for fetched_apartment in fetched_apartments:
            if convert_iso_date_to_python_date(fetched_apartment.date) < stop_date:
                continue
            contains = False
            for apartment_from_db in apartments:
                if apartment_from_db.link == fetched_apartment.link:
                    contains = True
                    break

            if not contains:
                for apartment_to_be_saved in apartments_to_be_saved:
                    if fetched_apartment.link == apartment_to_be_saved.link:
                        contains = True
                        break
                if not contains:
                    apartments_to_be_saved.append(fetched_apartment)

        db.insert_many(apartments_to_be_saved)
        logging.debug('Saved apartments {}'.format(apartments_to_be_saved))
        members = vk_api.getMembers().json()['response']['items']

        for apartment in apartments_to_be_saved:
            vk_api.sendMessageToMembers(members, format_apartment_message(apartment))

    except Exception as e:
        logging.error(e)
    time.sleep(300)
