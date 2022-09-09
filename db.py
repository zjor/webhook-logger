import os
import uuid
import psycopg2
import datetime


def get_connection():
    DATABASE_URL = os.environ['DATABASE_URL']
    return psycopg2.connect(DATABASE_URL, sslmode='require')


def run_migrations(conn):
    migrations = [
        """
        CREATE TABLE IF NOT EXISTS entities (
            id VARCHAR(64) PRIMARY KEY,
            "name" VARCHAR(255) NOT NULL,
            payload JSONB NOT NULL,
            "timestamp" TIMESTAMP NOT NULL
        )
        """
    ]
    with conn.cursor() as cursor:
        for m in migrations:
            cursor.execute(m)
    conn.commit()


def row_to_dict(row):
    return {
        'id': row[0],
        'name': row[1],
        'payload': row[2],
        'timestamp': row[3]
    }


def save_payload(conn, name, payload):
    _id = uuid.uuid4()
    query = f"INSERT INTO entities (id, \"name\", payload, \"timestamp\")" \
            f"VALUES ('{_id}', '{name}', '{payload}', '{datetime.datetime.now()}')"
    with conn.cursor() as cursor:
        cursor.execute(query)
    conn.commit()
    return _id


def find_by_id(conn, _id):
    query = f"SELECT id, \"name\", payload, \"timestamp\" FROM entities WHERE id = '{_id}'"
    with conn.cursor() as cursor:
        cursor.execute(query)
        return row_to_dict(cursor.fetchone())


def find_all_by_name(conn, name, timestamp_asc: bool = False):
    order_dir = 'ASC' if timestamp_asc else 'DESC'
    query = f"SELECT id, \"name\", payload, \"timestamp\" FROM entities WHERE \"name\" = '{name}' ORDER BY \"timestamp\" {order_dir}"
    result = []
    with conn.cursor() as cursor:
        cursor.execute(query)
        for row in cursor.fetchall():
            result.append(row_to_dict(row))
    return result


if __name__ == "__main__":
    conn = get_connection()
    run_migrations(conn)
    save_payload(conn, 'acme', '{"attr": "last3"}')
    for e in find_all_by_name(conn, 'acme', timestamp_asc=False):
        print(e)

    conn.close()
