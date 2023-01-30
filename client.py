import psycopg2

def create_db(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS clients(
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(33) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        email VARCHAR(40) NOT NULL);
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS phones(
        id_phone SERIAL PRIMARY KEY,
        client_id INT NOT NULL REFERENCES client(id),
        phone INT (10) NOT NULL UNIQUE);
    """)

    cur.commit()

def add_client(cur, first_name, last_name, email):
    INSERT INTO client(first_name, last_name, email)
    VALUES(%s, %s, %s);
    """, (first_name, last_name, email))
    cur.commit()

def add_phone(cur, client_id, phone):
    INSERT INTO phones(client_id, phone)
    VALUES(%s, %s);
    """, (client_id, phone))
    cur.commit()

def add_phone(cur, client_id, phone):
    cur.execute("""
    INSERT INTO phones(client_id, phone)
    VALUES (%s, %s) RETURNING phone;
    """, (client_id, phone))
    cur.commit()

def search_client(cur, first_name=None, last_name=None, email=None, phone=None):
    if not first_name:
        first_name = '%'
    if not last_name:
        last_name = '%'
    if not email:
        email = '%'
    if not phone:
        cur.execute("""
            SELECT id, first_name, last_name, email, phone FROM clients
            LEFT JOIN phones ON clients.id = phones.client_id
            WHERE first_name LIKE %s AND last_name LIKE %s AND
            email LIKE %s;
            """, (first_name, last_name, email))
    else:
        cur.execute("""
            SELECT id, first_name, last_name, email, phone FROM clients
            LEFT JOIN phones ON clients.id = phones.client_id
            WHERE phone = %s;
            """, (phone,))
    return cur.fetchall()

def change_client(cur, id, first_name=None, last_name=None, email=None, phone=None):
    print("Выберите тип данных для изменения и введите одну цифру от 1 до 4.\n "
        "1- имя клиента, 2 - фамилия клиента, 3- email клиента, 4- номер телефона клиента")

    while True:
        change_type = int(input())
        if change_type == 1:
            id_change_name = input("Укажите id клиента для изменения имени: ")
            new_first_name = input("Укажите новое имя: ")
            cur.execute("""
            UPDATE clients SET first_name=%s WHERE id=%s;
            """, (new_first_name, id_change_name))
            break
        elif change_type == 2:
            id_change_last_name = input("Укажите id клиента для изменения фамилии: ")
            new_last_name = input("Укажите новую фамилию: ")
            cur.execute("""
            UPDATE clients_ SET last_name=%s WHERE id=%s;
            """, (new_last_name, id_change_last_name))
            break
        elif change_type == 3:
            id_change_email = input("Укажите id клиента для изменения email: ")
            new_email = input("Укажите новый email: ")
            cur.execute("""
            UPDATE clients SET email=%s WHERE id=%s;
            """, (new_email, id_change_email))
            break
        elif change_type == 4:
            phone_to_change = input("Укажите номер телефона для его замены: ")
            new_phone = input("Укажите новый номер телефона: ")
            cur.execute("""
            UPDATE telephones SET phone=%s WHERE phone=%s;
            """, (new_phone, phone_to_change))
            break
        else:
            print(f"Введена неверная команда, поторите попытку. {change_client()}")

def delete_phone(cur, client_id, phone):
    id_delete_phone = input("Укажите id клиента для удаления номера: ")
    phone_for_delete = input("Какой номер телефона хотите удалить: ")
    with conn.cursor() as cur:
        cur.execute("""
           DELETE FROM phone WHERE client_id=%s AND phone=%s
           """, (id_delete_phone, phone_for_delete))

def delete_client(cur, client_id):
    id_delete_client = input("Укажите id клиента которого хотите удалить: ")
    last_name_delete_client = input("Укажите фамилию клиента которого хотите удалить: ")
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM phone WHERE client_id=%s
        """, (id_delete_client,))
        cur.execute("""
        DELETE FROM clients WHERE id=%s AND last_name=%s
        """, (id_delete_client, last_name_delete_client))

    return cur.fetchall()

with psycopg2.connect(database='client_db', user='postgres', password='1331') as conn:
    with conn.cursor() as cur:
        create_db(cur)
        add_client(cur, "Victor", "Gugo", "vigo@gmail.com")
        add_client(cur, "Arhip", "Kuingi", "arhku@mail.ru")
        add_client(cur, "Ilya", "Repin", "repka@mail.ru")
        add_client(cur, "Klod", "Mone", "eklmn@gmail.com")
        add_phone(cur, 1, "9657773890")
        add_phone(cur, 2, "9657773690")
        add_phone(cur, 3, "9657773793")
        add_phone(cur, 4, "9657773895")
        search_client()
        change_client()
        delete_phone()
        delete_client()

conn.close()
