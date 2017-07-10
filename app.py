import os
import logging
from flask import Flask, Response, json, request
from dotenv import Dotenv
from uuid import uuid5, uuid1
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
    
def connect():
    try:
        cursor = pymysql.cursors.DictCursor
        conn = pymysql.connect(RDS_HOST, user=NAME, passwd=PASSWORD, db=DB_NAME, port=RDS_PORT, cursorclass=cursor, connect_timeout=5)
        logger.info("SUCCESS: connection to RDS successful")
        return conn 
    except Exception as e:
        logger.exception("Database Connection Error")

def validate(data):
    error_fields = []
    not_null = [
        "first_name",
        "last_name",
        "email"
    ]

    for x in not_null:
        if x not in data or len(data[x]) == 0:
            error_fields.append(x)
    return (len(error_fields) == 0, error_fields)

def build_db():
    conn = connect()
    with conn.cursor() as cur:
        cur.execute("drop table if exists User")
        cur.execute("create table User ( ID varchar(255) NOT NULL, FirstName varchar(255) NOT NULL, LastName varchar(255) NOT NULL, Email varchar(255) NOT NULL, PRIMARY KEY (ID))")
        conn.commit()
    return build_response({"message": "success"}, 200)

def insert(data):
    uniq_id = str(uuid5(uuid1(), str(uuid1())))
    query = """insert into User (ID, FirstName, LastName, Email)
            values(%s, %s, %s, %s)
            """
    return (query, (uniq_id, data["first_name"], data["last_name"], data["email"]))

def build_response(resp_dict, status_code):
    response = Response(json.dumps(resp_dict), status_code)
    return response
        
@app.route('/')
def index():
    return build_response({"message": "Welcome to my lambda app!"}, 200)

@app.route('/build')
def build():
    return build_db()

@app.route('/user', methods=["GET", "POST"])
def user():
    conn = connect()
    if request.method == "GET":
        items = []
        try:
            with conn.cursor() as cur:
                cur.execute("select * from User")
                for row in cur:
                    items.append(row)
                conn.commit()
        except Exception as e:
            logger.info(e)
            response = build_response({"status": "error", "message": "error getting users"}, 500)
            return response
        finally:
            conn.close()
        response = build_response({"rows": items, "status": "success"}, 200)
        return response
    if request.method == "POST":
        data = {
            "first_name": request.form.get("first_name", ""),
            "last_name": request.form.get("last_name", ""),
            "email": request.form.get("email", "")
        }
        valid, fields = validate(data)
        if not valid:
            error_fields = ', '.join(fields)
            error_message = "Data missing from these fields: %s" %error_fields
            return build_response({"status": "error", "message": error_message}, 400)
        query, vals = insert(data)
        try:
            with conn.cursor() as cur:
                cur.execute(query, vals)
                conn.commit()
        except Exception as e:
            logger.exception("insert error")
            return build_response({"status": "error", "message": "insert error"}, 500)
        finally:
            conn.close()
            cur.close()
        return build_response({"status": "success"}, 200)
                        
if __name__ == '__main__':
    app.run()
