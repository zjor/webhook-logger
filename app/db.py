import os
import uuid
import logging
import psycopg2
import datetime

logging.basicConfig(level=logging.INFO)

SCHEMA_VERSION = 3


def get_connection():
    DATABASE_URL = os.environ['DATABASE_URL']
    ssl_mode = os.environ.get('SSL_MODE', 'require')
    return psycopg2.connect(DATABASE_URL, sslmode=ssl_mode, options='-c statement_timeout=10000')


def should_run_migration():
    with get_connection() as conn:
        try:
            query = 'SELECT "version" FROM schema_version'
            with conn.cursor() as c:
                c.execute(query)
                current_version = c.fetchone()[0]
                logging.info(f"Schema version: {current_version}")
                return SCHEMA_VERSION > current_version
        except Exception as e:
            logging.warning(f"Failed to detect schema version: {e}")
            return True


def run_migrations():
    migrations = [
        """
        CREATE TABLE IF NOT EXISTS entities (
            id VARCHAR(64) PRIMARY KEY,
            "name" VARCHAR(255) NOT NULL,
            payload JSONB NOT NULL,
            "timestamp" TIMESTAMP NOT NULL
        )
        """,
        """
        ALTER TABLE entities ADD COLUMN headers JSONB
        """,
        """
        CREATE TABLE IF NOT EXISTS schema_version (
            id INT PRIMARY KEY,
            "version" INT NOT NULL DEFAULT 1
        )
        """,
        f"""
        INSERT INTO schema_version (id, "version")
        VALUES (1, {SCHEMA_VERSION})
        ON CONFLICT (id)
        DO
            UPDATE SET "version" = {SCHEMA_VERSION} 
        """
    ]
    with get_connection() as conn:
        with conn.cursor() as cursor:
            for m in migrations:
                cursor.execute(m)
        conn.commit()


def update_schema():
    if should_run_migration():
        logging.info("Running migrations")
        run_migrations()
    else:
        logging.info("Schema is up to date")


def row_to_dict(row):
    if not row:
        return None
    return {
        'id': row[0],
        'name': row[1],
        'payload': row[2],
        'headers': row[3],
        'timestamp': row[4]
    }


def save_payload(conn, name, payload, headers):
    _id = uuid.uuid4()
    query = f"INSERT INTO entities (id, \"name\", payload, headers, \"timestamp\")" \
            f"VALUES ('{_id}', '{name}', '{payload}', '{headers}', '{datetime.datetime.now()}')"
    with conn.cursor() as cursor:
        cursor.execute(query)
    conn.commit()
    return _id


def find_by_id(conn, _id):
    query = f"SELECT id, \"name\", payload, headers, \"timestamp\" FROM entities WHERE id = '{_id}'"
    with conn.cursor() as cursor:
        cursor.execute(query)
        return row_to_dict(cursor.fetchone())


def find_all_by_name(conn, name, limit: int = None, timestamp_asc: bool = False):
    order_dir = 'ASC' if timestamp_asc else 'DESC'
    query = f"""
        SELECT id, \"name\", payload, headers, \"timestamp\" 
        FROM entities WHERE \"name\" = '{name}' 
        ORDER BY \"timestamp\" {order_dir}
    """
    if limit:
        query += f" LIMIT {limit}"
    result = []
    with conn.cursor() as cursor:
        cursor.execute(query)
        for row in cursor.fetchall():
            result.append(row_to_dict(row))
    return result


def get_schema_version(conn) -> int:
    query = 'SELECT "version" FROM schema_version'
    with conn.cursor() as c:
        c.execute(query)
        return c.fetchone()[0]


def get_total_count(conn) -> int:
    query = "SELECT count(*) FROM entities"
    with conn.cursor() as c:
        c.execute(query)
        return c.fetchone()[0]


def get_names_count(conn) -> int:
    query = """
    SELECT count(*) FROM 
        (SELECT DISTINCT "name" FROM entities) t
    """
    with conn.cursor() as c:
        c.execute(query)
        return c.fetchone()[0]


if __name__ == "__main__":
    update_schema()
