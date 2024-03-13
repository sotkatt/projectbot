import psycopg2
from os import getenv
from dotenv import load_dotenv
load_dotenv()


database = {
    'host': getenv('HOST'),
    'user': getenv('USER'),
    'password': getenv('PASSWORD'),
    'database': getenv('DATABASE'),
    'port': getenv('PORT')
}


def search_title(title):
    with psycopg2.connect(**database) as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"select * from places where title like '{title}%' or title like '%{title}%' or title like '%{title}'")
            place = cur.fetchall()

            if place is not None:
               return place

        return None
      

def get_user(user_id):
    with psycopg2.connect(**database) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM users WHERE user_id = %s",
                (user_id,)
            )
            user = cur.fetchone()
            if user is not None:
                return user
            
            return None


def registration_user(user_id, first_name, last_name, username, phone_number):
    with psycopg2.connect(**database) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "CREATE TABLE IF NOT EXISTS users(\
                    id SERIAL PRIMARY KEY,\
                    user_id BIGINT NOT NULL,\
                    first_name VARCHAR(125) DEFAULT NULL,\
                    last_name VARCHAR(125) DEFAULT NULL,\
                    username VARCHAR(125) DEFAULT NULL,\
                    phone_number VARCHAR(125) DEFAULT NULL,\
                    is_admin BOOLEAN DEFAULT FALSE,\
                    date TIMESTAMP DEFAULT current_timestamp)"
            )

            cur.execute(
                "INSERT INTO users(\
                    user_id, first_name, last_name, username, phone_number\
                ) VALUES (%s, %s, %s, %s, %s)", 
                (user_id, first_name, last_name, username, phone_number)
            )

            conn.commit()

            
def create_places(title, address, category, minprice, url):
    with psycopg2.connect(**database) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "CREATE TABLE IF NOT EXISTS places(\
                    id SERIAL PRIMARY KEY,\
                    title VARCHAR(125) DEFAULT NULL,\
                    address VARCHAR(125) DEFAULT NULL,\
                    category VARCHAR(125) DEFAULT NULL,\
                    minprice VARCHAR(125) DEFAULT NULL,\
                    url VARCHAR(125) DEFAULT NULL,\
                    date TIMESTAMP DEFAULT current_timestamp)"
            )

            cur.execute(
                f"select * from places where title = '{title}'"
            )
            place = cur.fetchone()

            if place is None:
                cur.execute(
                    "INSERT INTO places(\
                        title, address, category, minprice, url\
                    ) VALUES (%s, %s, %s, %s, %s)",
                    (title, address, category, minprice, url)
                )

                conn.commit()