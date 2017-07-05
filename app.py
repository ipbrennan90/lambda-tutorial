import os
import logging
from flask import Flask, Response, json, request
from dotenv import Dotenv
import pymysql
# Of course, replace by your correct path
dotenv = Dotenv(os.path.join(os.path.dirname(__file__), ".env"))
os.environ.update(dotenv)

app = Flask(__name__)
RDS_HOST = os.environ.get("DB_HOST")
RDS_PORT = int(os.environ.get("DB_PORT", 3306))
NAME = os.environ.get("DB_USERNAME")
PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def build_db():
    conn = connect()
    query = "create table User (ID int NOT NULL, firstName varchar(255) NOT NULL, lastName varchar(255) NOT NULL, email varchar(255), PRIMARY KEY (ID))"
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
    except Exception as e:
        logger.exception("could not build table")
    finally:
        cur.close()
        conn.close()
        response = Response(json.dumps({"message": "succes"}), 200)
        return response
        
    
def connect():
    try:
        cursor = pymysql.cursors.DictCursor
        conn = pymysql.connect(RDS_HOST, user=NAME, passwd=PASSWORD, db=DB_NAME, port=RDS_PORT, cursorclass=cursor, connect_timeout=5)
        logger.info("SUCCESS: connection to RDS successful")
        return(conn)
    except Exception as e:
        logger.exception("Database Connection Error")
        
@app.route('/')
def index():
    return "Hello World!", 200

@app.route('/build', methods=["GET"])
def build():
    build_db()
 
@app.route('/user', methods=["GET", "POST"])
def user():
    resp_dict = {}
    if request.method == "GET":
        resp_dict = {"first_name": "John", "last_name": "doe"}
    if request.method == "POST":
        data = request.form
        first_name = data.get("first_name", "")
        last_name = data.get("last_name", "")
        email = data.get("email", "")
        resp_dict = {"first_name": first_name, "last_name": last_name, "email": email}
    response = Response(json.dumps(resp_dict), 200)
    return response
    
                        
if __name__ == '__main__':
    app.run()
