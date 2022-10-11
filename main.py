import psycopg2
import config


# Дропнуть, если что :)
def drop_all():
    with psycopg2.connect(database=config.mybase, user=config.myuser, password=config.mypass) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                   DROP TABLE IF EXISTS numbers;
                   DROP TABLE IF EXISTS customers;
                   """)
            conn.commit()
    conn.close()


# Функция, создающая структуру БД (таблицы)
def create_db():
    with psycopg2.connect(database=config.mybase, user=config.myuser, password=config.mypass) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                   CREATE TABLE IF NOT EXISTS customers(
                       id SERIAL PRIMARY KEY,
                       name VARCHAR(40),
                       surname VARCHAR(40),
                       email VARCHAR
                       UNIQUE
                   );
                   """)
            cur.execute("""
                   CREATE TABLE IF NOT EXISTS numbers(
                       customer_id INTEGER REFERENCES customers(id) ON DELETE CASCADE,
                       number VARCHAR(11) NOT NULL
                       UNIQUE
                   );
                   """)
            conn.commit()
    conn.close()


# Функция, позволяющая добавить нового клиента
def add_customer(name, surname, email):
    with psycopg2.connect(database=config.mybase, user=config.myuser, password=config.mypass) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                   INSERT INTO customers(name, surname, email) VALUES(%s, %s, %s) RETURNING id;
                   """, (name, surname, email))
            print(f'Запись создана с ID - {cur.fetchone()[0]}')
    conn.close()


# Функция, позволяющая добавить телефон для существующего клиента
def add_number(customer_id, number):
    with psycopg2.connect(database=config.mybase, user=config.myuser, password=config.mypass) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                   INSERT INTO numbers(customer_id, number) VALUES(%s, %s);
                   """, (customer_id, number))
            cur.execute("""
            SELECT name, surname FROM customers WHERE id=%s;
            """, (customer_id,))
            print(f'Номер {number} добавлен для клиента {" ".join(list(cur.fetchone()))} c ID - {customer_id}')
            conn.commit()
    conn.close()


# Функция, позволяющая изменить данные о клиенте
def update_information(customer_id, data_type, data):
    with psycopg2.connect(database=config.mybase, user=config.myuser, password=config.mypass) as conn:
        with conn.cursor() as cur:
            if data_type == "name":
                cur.execute("""
                       UPDATE customers SET name=%s WHERE id=%s;
                       """, (data, customer_id))
                conn.commit()
            elif data_type == "surname":
                cur.execute("""
                                   UPDATE customers SET surname=%s WHERE id=%s;
                                   """, (data, customer_id))
                conn.commit()
            else:
                cur.execute("""
                                   UPDATE customers SET email=%s WHERE id=%s;
                                   """, (data, customer_id))
                conn.commit()
    conn.close()


# Второй вариант решения, но не понял почему f-строка работает, а %s не работает
def update_information_alter(customer_id, data_type, data):
    with psycopg2.connect(database=config.mybase, user=config.myuser, password=config.mypass) as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
                   UPDATE customers SET {data_type}=%s WHERE id=%s;
                   """, (data, customer_id))
            conn.commit()
    conn.close()


# Функция, позволяющая удалить телефон для существующего клиента
def delete_number(number):
    with psycopg2.connect(database=config.mybase, user=config.myuser, password=config.mypass) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                   DELETE FROM numbers WHERE number=%s
                   """, (number,))
            conn.commit()
    conn.close()


# Функция, позволяющая удалить существующего клиента
def delete_customer(user_id):
    with psycopg2.connect(database=config.mybase, user=config.myuser, password=config.mypass) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                   DELETE FROM customers WHERE id=%s;
                   """, (user_id,))
            conn.commit()
    conn.close()

# Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону)
def search(data_type, data):
    with psycopg2.connect(database=config.mybase, user=config.myuser, password=config.mypass) as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
                   SELECT name, surname, email, number FROM customers
                   JOIN numbers ON numbers.customer_id = customers.id
                   WHERE {data_type} = %s;
                   """, (data,))
            conn.commit()
            print(f'Поиск дал результат: {" ".join(list(cur.fetchall()[0]))}')
    conn.close()

drop_all()
create_db()
add_customer("Alexandr", "Pushkin", "alexandr@gmail.com")
add_customer("Mikhail", "Podgorny", "mikhail@mail.ru")
add_customer("Prohor", "Shalyapin", "mpodgorniy@mail.ru")
add_number("1", "89031331313")
add_number("2", "89051551515")
add_number("3", "89071771717")
update_information(1, "surname", "Podgorniy")
update_information_alter(2, "surname", "Pushkin")
delete_number("89051551515")
delete_customer(3)
search("name", "Alexandr")