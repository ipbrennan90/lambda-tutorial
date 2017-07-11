# Routing With Lambda and Flask

In this branch we will cover basic routing for a flask app deployed with zappa,
you should have covered the branch hello-world before starting here or be
familiar with zappa deployment and setting up a basic flask app


## Dependencies


## Get
first we need to add Response and json to our flask import:

```python
from flask import Flask, Response, json'
```

adding a get route is pretty straightforward with flask, let's add one for
getting a fake user:
```python
@app.route('/user', methods=["GET"])
def user():
    resp_dict = {"first_name": "John", "last_name": "doe"}
    response = Response(json.dumps(resp_dict), 200)
    return response
```

let's run that locally and check that everything is A-OK


```bash
export FLASK_APP=app.py
flask run
```

navigate to http://localhost:5000/get-user you should see:

```json
{
    "first_name": "John",
    "last_name": "Doe"
}
```

and that's it, we can update or zappa function now with:

```bash
zappa update
```

## Post

we'll need request from flask for this so add it to the import:

```python
from flask import Flask, Response, json, request
```

add the post method to your methods list and adjust your route function:

```python
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
```

you can run this locally and hit it with postman or another gui you like for
making requests, just make sure you are requesting with form-data or it won't work

once everything is good, zappa update and try out post and get on the lambda function
