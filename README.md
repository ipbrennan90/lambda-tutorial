# Routing requests to the Database

## Posting to the database with form data

first lets break out our response building into a function

```python
def build_response(resp_dict, status_code):
    response = Response(json.dumps(resp_dict), status_code)
    return response
```

next we're going to need to implement the post request response inside of our
user function

```python
def user():
    conn = connect()
    if request.method == "GET":
        # respond to get, coming soon
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
```

As you can see, we're missing our insert function and our validate function,

our validate function will validate our data object for insertion:

```python
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
```

this returns a boolean letting us know if our data is valid as well as a list
of fields that are missing from our data.

next, we need to write a simple insert query:

```python
def insert(data):
    uniq_id = str(uuid5(uuid1(), str(uuid1())))
    query = """insert into User (ID, FirstName, LastName, Email)
            values(%s, %s, %s, %s)
            """
    return (query, (uniq_id, data["first_name"], data["last_name"], data["email"]))

```
update your function,

```bash
zappa update

```
now we should be able to post to our lambda function user endpoint, I used postman
to do so but anything works, and we should see a success callback.

## Get request for users in RDS

For the get request we just want to return a json representation of our user
table, this can be achieved easily by adding get request handling to our user
function

```python
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
```

then, as always:

```bash
zappa update

```

now I recommend getting a json prettifier extension like [json-viewer](https://github.com/tulios/json-viewer)
to see an easily digestable repersentation of your database within your browser.
Once you have an extension enabled visit your user endpoint in your browser and
you should be seeing your user table in json form like so:

![Alt text](/../screenshots/screenshots/user-json.png?raw=true "user-json")


I was aided alot by [this](http://docs.aws.amazon.com/lambda/latest/dg/vpc-rds.html)
amazon tutorial while writing this branch.
