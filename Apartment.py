class Apartment:
    def __init__(self, link, price, title, date):
        self.link = link
        self.price = price
        self.title = title
        self.date = date

    def __str__(self):
        return '{link: ' + self.link + ' title: ' + self.title + ' price: ' + self.price + ' date: ' + self.date + '}'

    def __repr__(self):
        return '{link: ' + self.link + ' title: ' + self.title + ' price: ' + self.price + ' date: ' + self.date + '}'


