import psycopg2

# Функция, создающая структуру БД (таблицы)
def create_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS customer(
            customer_id SERIAL PRIMARY KEY,
            first_name VARCHAR(40),
            last_name VARCHAR(40),
            email VARCHAR(40)
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS phone(
            phone_id SERIAL PRIMARY KEY,
            phone_number VARCHAR(10),
            customer_id INTEGER REFERENCES customer(customer_id) ON DELETE CASCADE NOT NULL
        );
        """)
        conn.commit()

# Функция, позволяющая добавить нового клиента
def add_customer(conn, first_name, last_name, email):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO customer(first_name, last_name, email) VALUES(%s, %s, %s);
        """, (first_name, last_name, email))
        conn.commit()

# Функция, позволяющая добавить телефон для существующего клиента
def add_phone_number(conn, customer_id, phone_number):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO phone(customer_id, phone_number) VALUES(%s, %s);
        """, (customer_id, phone_number))
        conn.commit()

# Функция, позволяющая изменить данные о клиенте
def change_data(conn, customer_id, first_name=None, last_name=None, email=None):
    with conn.cursor() as cur:
        cur.execute("""
        UPDATE customer SET first_name=%s, last_name=%s, email=%s WHERE customer_id=%s;
        """, (first_name, last_name, email, customer_id))
        conn.commit()

# Функция, позволяющая удалить телефон для существующего клиента
def delete_phone_number(conn, customer_id, phone_number):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM phone WHERE customer_id=%s AND phone_number=%s;
        """, (customer_id, phone_number))
        conn.commit()

# Функция, позволяющая удалить существующего клиента
def delete_customer(conn, customer_id):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM customer WHERE customer_id=%s;
        """, (customer_id,))
        conn.commit()

# Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону
def find_customer(conn, first_name=None, last_name=None, email=None, phone_number=None):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT * FROM phone p 
        JOIN customer c ON p.customer_id = c.customer_id
        WHERE first_name=%s OR last_name=%s OR email=%s OR phone_number=%s;
        """, (first_name, last_name, email, phone_number))
        print(cur.fetchall())

# Вызов функций 
with psycopg2.connect(database='customer_db', user='postgres', password='postgres') as conn:
    # Создание таблиц
    create_table(conn)
    
    # Добавление новых клиентов
    add_customer(conn, 'Мария', 'Плотникова', 'MaryPlotnik@smth.com')
    add_customer(conn, 'Дмитрий', 'Зубарев', 'Zuba@smth.com')
    add_customer(conn, 'Максим', 'Минимумов', 'MaxMin@smth.com')
    add_customer(conn, 'Нина', 'Иванова', 'IvaNina@smth.com')
    add_customer(conn, 'Елизавета', 'Смирнова', 'ElizavetaSmirnova@smth.com')
    add_customer(conn, 'Виктор', 'Кравец', 'ViktorKravec@smth.com')

    # Добавление телефонных номеров клиентов
    add_phone_number(conn, 1, '9321436823')
    add_phone_number(conn, 1, '9321427823')
    add_phone_number(conn, 2, '9121436070')
    add_phone_number(conn, 3, '9500013129')
    add_phone_number(conn, 4, '9092788800')
    add_phone_number(conn, 4, '9001368018')
    add_phone_number(conn, 5, '9119283467')
    add_phone_number(conn, 6, '9329009999')
    add_phone_number(conn, 6, '9329209303')

    # Изменение информации о клиенте
    change_data(conn, 4, 'Нина', 'Иванова', 'IvanovaNina@smth.com')

    # Удаление телефонного номера клиента
    delete_phone_number(conn, 4, '9001368018')

    # # Удаление существующего клиента
    delete_customer(conn, 1)

    # Поиск клиента по его данным
    find_customer(conn, first_name='Виктор')
    find_customer(conn, last_name='Зубарев')
    find_customer(conn, email='ViktorKravec@smth.com')
    find_customer(conn, phone_number='9321436823')

conn.close()