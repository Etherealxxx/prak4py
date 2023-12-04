import sqlite3
import os
import time

conn_users = sqlite3.connect('database.db')
cursor_users = conn_users.cursor()

cursor_users.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT UNIQUE,
        password TEXT
    )
''')
conn_users.commit()

conn_order = sqlite3.connect('database.db')
cursor_order = conn_order.cursor()

cursor_order.execute('''
    CREATE TABLE IF NOT EXISTS basket_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        stop_list BOOLEAN DEFAULT 0
    )
''')
conn_order.commit()

conn_reviews = sqlite3.connect('database.db')
cursor_reviews = conn_reviews.cursor()


cursor_reviews.execute('''
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        item_name TEXT,
        review TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
''')
conn_reviews.commit()

conn_delivery = sqlite3.connect('database.db')
cursor_delivery = conn_delivery.cursor()

cursor_delivery.execute('''
    CREATE TABLE IF NOT EXISTS delivery (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        address TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
''')
conn_delivery.commit()

basket = []

def jober(login: str, password: str):
    try:
        cursor_users.execute("INSERT INTO users (login, password) VALUES (?, ?)", (login, password))
        conn_users.commit()
        return f"Пользователь {login} успешно добавлен"
    except sqlite3.Error as e:
        return "Ошибка добавления пользователя"

def showuser(login: str, password: str):
    cursor_users.execute("SELECT * FROM users WHERE login=? AND password=?", (login, password))
    return cursor_users.fetchone()

def add_review(item_name):
    review = input(f"Оставьте отзыв для продукта '{item_name}': ")
    cursor_reviews.execute('''
        INSERT INTO reviews (item_name, review) VALUES (?, ?)
    ''', (item_name, review))
    conn_reviews.commit()
    print("Отзыв успешно добавлен!")


def add_to_basket(item_name):
    global basket

    stop_list_items = ["Сырные колечки", "Биг спешиал"]

    if item_name in stop_list_items:
        stop_list = 1
        print(f"Эта позиция ({item_name}) находится в стоп-листе!")
    else:
        stop_list = 0

    basket.append(item_name)

    cursor_order.execute('''
        INSERT INTO basket_items (item_name, stop_list) VALUES (?, ?)
    ''', (item_name, stop_list))
    conn_order.commit()


def display_basket():
    print("Текущая корзина:", basket)

def save_credentials(login, password):
    with open('credentials.txt', 'w') as file:
        file.write(f'{login}\n{password}')

def register_user():
    print('Введите логин:')
    login = input()

    print('Введите пароль:')
    password = input()

    print('Повторите пароль:')
    password_repeat = input()

    if password != password_repeat:
        print('Пароли не совпадают!')
    else:
        result = jober(login, password)

        if result == "Ошибка добавления пользователя":
            print(result)
        else:
            print(result)
            login_user()


def login_user():
    while True:
        print('Введите логин:')
        login = input()

        print('Введите пароль:')
        password = input()

        result = showuser(login, password)

        if result:
            print('Вы вошли в оформление заказа Вкусно и Точка')
            user_id = result[0]  
            save_credentials(login, password)
            VIT(user_id)  
            break
        else:
            print('Неверный логин или пароль. Попробуйте снова.')


def login_or_register():
    while True:
        print('Выберите действие (1 - Вход, 2 - Регистрация, 3 - Вход для клиента, 4 - Выход): ')
        action = input()

        if action == '1':
            login_user()
            break
        elif action == '2':
            register_user()
            break
        elif action == '4':
            print('До свидания')
            exit()
        else:
            print('Некорректный выбор, пожалуйста, повторите.')

def VIT(user_id):
    item_name = None  

    while True:
        time.sleep(1)

        choice = input('''
            Выберите категорию:
                1. Новинки
                2. Популярное
                3. Напитки
                4. Картошка и стартеры
            ''')

        if choice == "1":
            choice2 = input(''' Выберите что-то из этого:
                   1. Скандинавский бургер
                   2. Биг спешиал
                   3. Кидз комбо
                    :''')
            if choice2 == '1':
                item_name = "Скандинавский бургер"
                add_to_basket(item_name)
                print(f"{item_name} добавлен в корзину!")
            elif choice2 == '2':
                item_name = "Биг спешиал"
                add_to_basket(item_name)
                print(f"{item_name} добавлен в корзину!")
                print("Эта позиция находится в стоп-листе. Выберите другую.")
                continue
            
            elif choice2 == '3':
                item_name = "Кидз комбо"
                add_to_basket(item_name)
                print(f"{item_name} добавлен в корзину!")
            else:
                print("Некорректный выбор, пожалуйста, повторите.")
                continue

        elif choice == "2":
            print('''Выберите что-то из популярного:
                   1. Биг хит
                   2. Гранд
                   3. Гранд де люкс''')
            choice_popular = input(": ")
            
            if choice_popular == '1':
                item_name = "Биг хит"
                add_to_basket(item_name)
                display_basket()
            elif choice_popular == '2':
                item_name = "Гранд"
                add_to_basket(item_name)
                display_basket()
            elif choice_popular == '3':
                item_name = "Гранд де люкс"
                add_to_basket(item_name)
                display_basket()
            else:
                print("Некорректный выбор, пожалуйста, повторите.")
                continue


        elif choice == "3":
            print('''Выберите что-то из напитков:
                   1. Добрый кола
                   2. Добрый апельсин
                   3. Молочный коктейль Ванильный''')
            choice_beverages = input(": ")
            
            if choice_beverages == '1':
                item_name = "Добрый кола"
                add_to_basket(item_name)
                display_basket()
            elif choice_beverages == '2':
                item_name = "Добрый апельсин"
                add_to_basket(item_name)
                display_basket()
            elif choice_beverages == '3':
                item_name = "Молочный коктейль Ванильный"
                add_to_basket(item_name)
                display_basket()
            else:
                print("Некорректный выбор, пожалуйста, повторите.")
                continue

        elif choice == "4":
            print('''Выберите что-то из картошки и стартеров:
                   1. Сырные колечки
                   2. Гранд фри
                   3. Снэк бокс''')
            choice_potatoes_starters = input(": ")
            
            if choice_potatoes_starters == '1':
                item_name = "Сырные колечки"
                add_to_basket(item_name)
                print("Эта позиция находится в стоп-листе. Выберите другую.")
                continue
            elif choice_potatoes_starters == '2':
                item_name = "Гранд фри"
                add_to_basket(item_name)
                display_basket()
            elif choice_potatoes_starters == '3':
                item_name = "Снэк бокс"
                add_to_basket(item_name)
                display_basket()
            else:
                print("Некорректный выбор, пожалуйста, повторите.")
                continue

        proceed = input("Желаете добавить еще что-то в корзину? (Да/Нет): ").lower()
        if proceed != 'да':
            if item_name:
                add_review(item_name)
            address = input("Введите адрес для доставки (если необходимо): ").strip()
            if address:
                save_delivery_address(user_id, address)
                break

def save_delivery_address(user_id, address):
    try:
        cursor_delivery.execute("INSERT INTO delivery (user_id, address) VALUES (?, ?)", (user_id, address))
        conn_delivery.commit()
        print("Адрес для доставки успешно сохранен!")
    except sqlite3.Error as e:
        print("Ошибка сохранения адреса для доставки:", e)

          
def welcome():
    print("Добро пожаловать во Вкусно и Точка")

    if os.path.exists('credentials.txt'):
        with open('credentials.txt', 'r') as file:
            login = file.readline().strip()
            password = file.readline().strip()
        result = showuser(login, password)
        if result:
            print(f'Автоматическая авторизация для админа {login}')
            VIT(result[0]) 
        else:
            print('Невозможно автоматически войти. Меню:')
            login_or_register()
    else:
        login_or_register()

def main():
    login_or_register()

if __name__ == "__main__":
    main()

conn_users.close()
conn_order.close()
conn_reviews.close()
conn_delivery.close()
