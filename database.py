import numpy as np
import psycopg2
import json
from datetime import datetime
from credentials import db_credentials

conn = psycopg2.connect(database=db_credentials["database"],
                        host=db_credentials["host"],
                        user=db_credentials["user"],
                        password=db_credentials["password"],
                        port=db_credentials["port"])

cursor = conn.cursor()

users_data = [
    ("alice", "pass123"),
    ("bob", "123pass"),
    ("charlie", "secret!"),
    ("david", "pw1234"),
    ("emma", "123password"),
    ("frank", "Password1"),
    ("grace", "Password2"),
    ("henry", "pwpwpw"),
    ("isabel", "123!!pw"),
    ("jack", "pw12345"),
    ("karen", "secret123"),
    ("lucas", "321secret"),
    ("molly", "PWSecret"),
    ("nathan", "pw_1234"),
    ("olivia", "passpass"),
    ("SECRET_USR_CHATG05", "FLAG")
]


def make_query(query: str, is_select=True):
    """ helper function to make queries """
    try:
        cursor.execute(query)
        if is_select:
            result = cursor.fetchall()
            return result
        else:
            conn.commit()
    except Exception as e:
        print("Error:", e)
        conn.rollback()


def close():
    """ helper function to close connection """
    cursor.close()
    conn.close()


## USERS ##


def create_users_table():
    """ helper function to create users table """
    create_table_query = """
    CREATE TABLE users (
        user_id serial PRIMARY KEY,
        username VARCHAR(50) NOT NULL,
        password VARCHAR(255) NOT NULL
    );
    """
    cursor.execute(create_table_query)
    conn.commit()


def drop_table(table: str):
    """ helper function to drop table """
    cursor.execute(f"DROP TABLE IF EXISTS {table};")
    conn.commit()


def clear_table(table: str):
    """ helper function to clear table """
    cursor.execute("DELETE FROM {table};")
    conn.commit()


def populate_users_table():
    """ helper function to populate user table """
    for username, password in users_data:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s);", (username, password))
    conn.commit()


## LOCATIONS ##


def create_locations_table():
    create_table_query = """
    CREATE TABLE locations (
        location_id serial PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        lat DECIMAL(9, 6) NOT NULL,
        lon DECIMAL(9, 6) NOT NULL,
        CONSTRAINT unique_name UNIQUE (name)
    );
    """
    create_secret_table_query = """
    CREATE TABLE secret_locations (
        location_id serial PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        lat DECIMAL(9, 6) NOT NULL,
        lon DECIMAL(9, 6) NOT NULL,
        CONSTRAINT unique_secret_name UNIQUE (name)
    );
    """
    cursor.execute(create_table_query)
    conn.commit()
    cursor.execute(create_secret_table_query)
    conn.commit()


def generate_location(no_users):
    """ helper function to generate random (x, y) points in sydney """
    sydney_lat, sydney_lon = -33.865143, 151.209900
    data = np.random.randn(no_users, 2) / [50, 50] + [sydney_lat, sydney_lon]
    return data


def populate_locations_table():
    """ helper function to populate locations table """
    names = ["Amy", "Scott", "Jerry"]
    locations_data = [[-33.84845253, 151.18314397],
                      [-33.88139486, 151.21065608], [-33.87767367, 151.18171362]]
    for i in range(3):
        name = names[i]
        lat, lon = locations_data[i]
        insert_query = """
            INSERT INTO locations (name, lat, lon)
            VALUES (%s, %s, %s)
            ON CONFLICT (name)
            DO UPDATE SET lat = EXCLUDED.lat, lon = EXCLUDED.lon;
        """
        cursor.execute(insert_query, (name, lat, lon))
        conn.commit()

    secret = ("Admin", -33.8984, 151.2359)
    insert_secret_query = """
            INSERT INTO secret_locations (name, lat, lon)
            VALUES (%s, %s, %s)
            ON CONFLICT (name)
            DO UPDATE SET lat = EXCLUDED.lat, lon = EXCLUDED.lon;
        """
    cursor.execute(insert_secret_query, secret)
    conn.commit()


## BLOG ##


def create_blog_table():
    """ helper function to create blog table """
    create_table_query = """
    CREATE TABLE blog (
    blog_id serial PRIMARY KEY,
    blog_title VARCHAR(255) NOT NULL,
    body TEXT NOT NULL,
    comments JSON NOT NULL
    );
    """
    cursor.execute(create_table_query)
    conn.commit()


def populate_blog_data():
    """ helper function to populate blog table """
    title = "Craving a 🍔 Hamburger"
    body = """Hamburgers, the best way to satisfy your hunger cravings!\n\nConsisting of a juicy beef patty, fresh and crispy veggies, ketchup and mayo, topped of with a toasty sesame seeded bun...\n\nJust one bite of a delicious mouth-watering hamburger will make your problems go away!\n"""
    comments = [
        {
            'name': 'Alice',
            'date': '17-10-2023 09:13:12',
            'comment': 'Mmmmm hamburgers...'
        },
        {
            'name': 'Bob',
            'date': '18-10-2023 15:45:30',
            'comment': 'Yum 😋!!'
        }
    ]

    insert_query = """
    INSERT INTO blog (blog_title, body, comments)
    VALUES (%s, %s, %s)
    """
    cursor.execute(insert_query, (title, body, json.dumps(comments)))
    conn.commit()


## BUILD DB ##


drop_table("users")
create_users_table()
populate_users_table()

drop_table("locations")
drop_table("secret_locations")
create_locations_table()
populate_locations_table()

drop_table("blog")
create_blog_table()
populate_blog_data()
