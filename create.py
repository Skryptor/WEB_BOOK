import sqlalchemy as sq
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import configparser
import json
from model import create_tables, STOCK, SALE, SHOP, BOOK, PUBLISHER

config = configparser.ConfigParser()
config.read('settings.ini')
password = config["password"]['password']

DSN = f'postgresql://postgres:{password}@localhost:5432/WEB_BOOK'

engine = sq.create_engine(DSN)
Session = sessionmaker(bind=engine)
session = Session()
create_tables(engine)

# writer = PUBLISHER(id = 1, name = "Pushkin A.S.")
# book1 = BOOK(id = 1, title = "Капитанская дочка", id_publisher = 1)
# book2 = BOOK(id = 2,title = "Руслан и Людмила", id_publisher = 1)
# book3 = BOOK(id = 3,title = "Евгений Онегин", id_publisher = 1)
# shop1 = SHOP(name = "Буквоед" )
# shop2 = SHOP(name = "Лабиринт" )
# shop3 = SHOP(name = "Книжный дом" )
# stock1 = STOCK(id_book = 1, id_shop = 1, count = 40)
# stock2 = STOCK(id_book = 2, id_shop = 1, count = 35)
# stock3 = STOCK(id_book = 1, id_shop = 2, count = 30)
# stock4 = STOCK(id_book = 3, id_shop = 3, count = 50)
# sales1 = SALE(price = 600, id_stock = 1, date_sale = "09-11-2022", count = 39)
# sales2 = SALE(price = 500, id_stock = 2, date_sale = "08-11-2022", count = 34)
# sales3 = SALE(price = 580, id_stock = 3, date_sale = "05-11-2022", count = 29)
# sales4 = SALE(price = 490, id_stock = 4, date_sale = "02-11-2022", count = 49)
# sales5 = SALE(price = 600, id_stock = 1, date_sale = "26-10-2022", count = 38)
# session.add_all([writer, book1, book2, book3, shop1, shop2, shop3, stock1, stock2, stock3, stock4, sales1, sales2, sales3, sales4, sales5])
# session.commit()

with open('netologi.json', encoding='utf-8') as f:
    data = json.load(f)

for record in data:
    model = {
        'publisher': PUBLISHER,
        'shop': SHOP,
        'book': BOOK,
        'stock': STOCK,
        'sale': SALE,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()
session.close()