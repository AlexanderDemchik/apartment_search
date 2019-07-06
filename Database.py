import sqlite3
from Apartment import Apartment
import logging


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('search_apartments')
        cursor = self.conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS apartments (link text, price text, title text, issueDate text)')

    def insert(self, apartment):
        logging.debug('INSERT TO APARTMENTS')
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO apartments(link, price, title, issueDate) VALUES ({}, {}, {}, {})'.format(apartment.link, apartment.price, apartment.title, apartment.date))

    def insert_many(self, apartments):
        logging.debug('INSERT MANY TO APARTMENTS')
        cursor = self.conn.cursor()
        cursor.executemany("INSERT INTO apartments VALUES (?, ?, ?, ?)", self.apartments_to_rows(apartments))
        self.conn.commit()

    def fetch(self):
        logging.debug('FETCH FROM APARTMENTS')
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM apartments ORDER BY datetime(issueDate) DESC')
        rows = cursor.fetchall()
        apartments = []
        for row in rows:
            apartments.append(Apartment(row[0], row[1], row[2], row[3]))

        return apartments

    def apartments_to_rows(self, apartments):
        result = []
        for apartment in apartments:
            result.append((apartment.link, apartment.price, apartment.title, apartment.date))

        return result
