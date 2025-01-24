from sqlalchemy.orm import sessionmaker

from model import BOOK, SHOP, SALE, STOCK, PUBLISHER
from create import engine

Session = sessionmaker(bind=engine)
session = Session()

search_option = input("Вы хотите искать по ID (1) или имени писателя (2)? Введите 1 или 2: ").strip()

if search_option == "1":
    search_id = input("Введите ID писателя: ").strip()
    query = (
        session.query(PUBLISHER.name, BOOK.title, SHOP.name, SALE.price, SALE.date_sale)
        .join(BOOK, PUBLISHER.id == BOOK.id_publisher)
        .join(STOCK, BOOK.id == STOCK.id_book)
        .join(SALE, STOCK.id == SALE.id_stock)
        .join(SHOP, STOCK.id_shop == SHOP.id)
        .filter(PUBLISHER.id == int(search_id))
        .order_by(SALE.date_sale)
    )
elif search_option == "2":
    search_name = input("Введите имя писателя: ").strip()
    query = (
        session.query(PUBLISHER.name, BOOK.title, SHOP.name, SALE.price, SALE.date_sale)
        .join(BOOK, PUBLISHER.id == BOOK.id_publisher)
        .join(STOCK, BOOK.id == STOCK.id_book)
        .join(SALE, STOCK.id == SALE.id_stock)
        .join(SHOP, STOCK.id_shop == SHOP.id)
        .filter(PUBLISHER.name.ilike(f"%{search_name}%"))  # Фильтр по имени писателя
        .order_by(SALE.date_sale)
    )
else:
    print("Неверный ввод. Завершение программы.")
    session.close()
    exit()

results = query.all()

if results:
    print("\nРезультаты поиска:")
    for writer_name, book_title, shop_name, price, date_sale in results:
        print(f"{writer_name:<20} | {book_title:<20} | {shop_name:<12} | {price:<4} | {date_sale.strftime('%d-%m-%Y')}")
else:
    print("\nНичего не найдено по вашему запросу.")

session.close()
