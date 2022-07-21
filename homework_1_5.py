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
        conn.commit()


def add_client(conn, first_name, last_name, email, phone=None):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO client(first_name, last_name, email)
            VALUES(%s, %s, %s)
            RETURNING id;
            """, (first_name, last_name, email))
        client_id = cur.fetchone()
        cur.execute("""
            INSERT INTO phone(client_id, phone)
            VALUES(%s, %s);
            """, (client_id, phone))
        cur.execute("""
            SELECT * FROM phone;
            """)
        print(cur.fetchall())


def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO phone(client_id, phone)
            VALUES(%s, %s);
            """, (client_id, phone))
        cur.execute("""
            SELECT * FROM phone;
            """)
        print(cur.fetchall())


def change_client(conn, client_id, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        if first_name is not None:
            cur.execute("""
                UPDATE client
                SET first_name = %s
                WHERE id = %s;
                """, (first_name, client_id))
        if last_name is not None:
            cur.execute("""
                UPDATE client
                SET last_name = %s
                WHERE id = %s;
                """, (last_name, client_id))
        if email is not None:
            cur.execute("""
                UPDATE client
                SET email = %s
                WHERE id = %s;
                """, (email, client_id))
        if phone is not None:
            cur.execute("""
                UPDATE phone
                SET phone = %s
                WHERE client_id = %s AND id =(
                    SELECT min(id)
                    FROM phone
                    WHERE client_id = %s)
                """, (phone, client_id, client_id))
        cur.execute("""
            SELECT * FROM client;
            """)
        print(cur.fetchall())


def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM phone
            WHERE phone = %s AND client_id = %s;
            """, (phone, client_id))
        cur.execute("""
            SELECT * FROM phone;
            """)
        print(cur.fetchall())


def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM phone
            WHERE client_id = %s;
            """, (client_id,))
        cur.execute("""
            DELETE FROM client
            WHERE id = %s;
            """, (client_id,))
        cur.execute("""
            SELECT * FROM client;
            """)
        print(cur.fetchall())


def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        #
        if phone is not None:
            cur.execute("""
                        SELECT c.id, c.first_name, c.last_name, c.email
                        FROM phone AS p
                        LEFT JOIN client AS c
                        ON p.client_id = c.id
                        WHERE p.phone = %s;
                        """, (phone,))
            print(cur.fetchall())
        elif email is not None:
            cur.execute("""
                        SELECT *
                        FROM client
                        WHERE email = %s;
                        """, (email,))
            print(cur.fetchall())
        elif first_name is not None and last_name is not None:
            cur.execute("""
                            SELECT *
                            FROM client
                            WHERE first_name = %s AND last_name =%s;
                            """, (first_name, last_name))
            print(cur.fetchall())
        elif first_name is not None:
            cur.execute("""
                                SELECT *
                                FROM client
                                WHERE first_name = %s;
                                """, (first_name,))
            print(cur.fetchall())
        elif last_name is not None:
            cur.execute("""
                                    SELECT *
                                    FROM client
                                    WHERE last_name = %s;
                                    """, (last_name,))
            print(cur.fetchall())


with psycopg2.connect(database="", user="", password="") as conn:
    create_db(conn)
    add_client(conn, 'Andrey', 'Halizev', 'a@halizev.ru', '796367931')
    add_client(conn, 'And', 'Hal', 'a@hal.ru', '7963')
    add_phone(conn, 1, '7800553535')
    change_client(conn, 1, first_name='Andr', phone=123)
    delete_phone(conn, 1, '7800553535')
    delete_client(conn, 1)
    find_client(conn, phone='7963')
    find_client(conn, email='a@hal.ru')
    find_client(conn, first_name='And', last_name='Hal')
conn.close()
