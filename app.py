import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request

CREATE_ROOMS_TABLE = (
    "CREATE TABLE IF NOT EXISTS ROOMS (id SERIAL PRIMARY KEY, name TEXT);"
)
CREATE_TEMPS_TABLE = """CREATE TABLE IF NOT EXISTS temperature (room_id INTEGER, temperature REAL,
                        date TIMESTAMP, FOREIGN key(room_id) REFERENCES rooms(id) on DELETE CASCADE);"""

INSERT_ROOM_RETURN_ID = "INSERT INTO rooms (name) VALUES (%s) RETURNING id;"

INSERT_TEMP = (
    "INSERT INTO temperatures (room_id, temperature, date) VALUES (%s, %s, %s);"
)

GLOBAL_NUMBER_OF_DAYS = (
    """SELECT COUNT(DISTINCT DATE(date) AS days FROM temperature;"""
)

GLOBAL_AVG = """SELECT AVG(temperature) as average FROM temperatures;"""



load_dotenv()


app =  Flask(__name__)
# url = os.getenv("DATABASE_URl")
url = "postgres://uhbtyeiq:T8YedkiAUIJ4TiQDnd3ePtP3cKkF9fG8@tiny.db.elephantsql.com/uhbtyeiq"
connection = psycopg2.connect(url)

@app.route('/')
def index():
    return 'Hello World'

@app.post("/api/room")
def create_room():
    data = request.get_json()
    name = data["name"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_ROOMS_TABLE)
            cursor.execute(INSERT_ROOM_RETURN_ID, (name,))
            room_id = cursor.fetchone()[0]
    return {"id": room_id, "message": f"Room {name} created."},201


if __name__ == '__main__':
    app.run()