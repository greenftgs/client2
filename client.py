import psycopg2

def create_db(conn):
    conn.execute("""
    CREATE TABLE IF NOT EXISTS clients(
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(33) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        email VARCHAR(40) NOT NULL);
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS phones(
        id_phone SERIAL PRIMARY KEY,
        client_id INT NOT NULL REFERENCES client(id),
        phone INT (10) NOT NULL UNIQUE);
    """)

    conn.commit()

def add_client(conn, first_name, last_name, email):
    INSERT INTO client(first_name, last_name, email)
    VALUES(%s, %s, %s);
    """, (first_name, last_name, email))
    conn.commit()

def add_phone(conn, client_id, phone):
    INSERT INTO phones(client_id, phone)
    VALUES(%s, %s);
    """, (client_id, phone))
    conn.commit()

def search_client(conn, first_name=None, last_name=None, email=None, phone=None):
    if not first_name:
        first_name = '%'
    if not last_name:
        last_name = '%'
    if not email:
        email = '%'
    if not phone:
        conn.execute("""
            SELECT id, first_name, last_name, email, phone FROM clients
            LEFT JOIN phones ON clients.id = phones.client_id
            WHERE first_name LIKE %s AND last_name LIKE %s AND
            email LIKE %s;
            """, (first_name, last_name, email))
    else:
        conn.execute("""
            SELECT id, first_name, last_name, email, phone FROM clients
            LEFT JOIN phones ON clients.id = phones.client_id
            WHERE phone = %s;
            """, (phone,))
    return conn.fetchall()

def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    UPDATE client SET name = %s WHERE id = %s;
    """, ('Python Advanced', python_id))

def delete_phone(conn, client_id, phone):
pass

def delete_client(conn, client_id):
pass

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
pass

with psycopg2.connect(database='client_db', user='postgres', password='1331') as conn:
with conn.cursor() as cur:

conn.close()