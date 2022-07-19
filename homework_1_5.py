import psycopg2

def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS client(
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(40),
                last_name VARCHAR(40),
                email VARCHAR(40)
            );
            CREATE TABLE IF NOT EXISTS phone(
                id SERIAL PRIMARY KEY,
                client_id INTEGER REFERENCES client(id),
                phone VARCHAR(40)
            );               
            """)
        conn.commit()  # фиксируем в БД

def add_client(conn, first_name, last_name, email, phones=None):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO client(first_name, last_name, email)
            VALUES(first_name, last_name, email);
            """)
        conn.commit()

def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO phone(client_id, phone)
            VALUES(client_id, phone);
            """)
        conn.commit()

def change_client(conn, client_id, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE client
            SET first_name=%s, last_name=%s, email=%s
            WHERE id=%s;
            """, (first_name, last_name, email, client_id))
        cur.execute("""
            UPDATE phone
            SET phone=%s
            WHERE id=%s;
            """, (phone, client_id))
        cur.execute("""
            SELECT * FROM client;
            """)

def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM phone
            WHERE phone=%s AND client_id=%s;
            """, (phone, client_id))
        cur.execute("""
            SELECT * FROM client;
            """)
        print(cur.fetchall())

def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM phone
            WHERE client_id=%s;
            """, (client_id,))
        cur.execute("""
            DELETE FROM client
            WHERE id=%s;
            """, (client_id,))
        cur.execute("""
            SELECT * FROM homework;
            """)
        print(cur.fetchall())

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT * FROM course;
            """)
        print('fetchall', cur.fetchall())


with psycopg2.connect(database="clients_db", user="postgres", password="postgres") as conn:

conn.close()