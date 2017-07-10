# Adding cors handling to your Lambda function

This is one of the shortest branches but cors is what gave me the
most trouble, and is ultimately necessary if you ever want to hit
your function from a client side app.

I tried using aws's automated cors setup, I tried wrapping the app
with the flask cors package. All of these presented their fair share
of headaches and since zappa sets your function up as a proxy it's a lot
more simple to just handroll your CORs headers and Options preflight request
handling.

## CORs headers

All I had to do to add cors headers is add two lines to my build_response function:

```
def build_response(resp_dict, status_code):
    response = Response(json.dumps(resp_dict), status_code)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response
```
## Handling preflight, or options requests.

When a Cross Origin Request comes in from an application it will first hit
your function with an Options request to do a pre-flight check and make sure
there's nothing malicious going on, we'll need to handle that by adding
a few things to our user function:

```python
def user():
    if request.method == "OPTIONS":
        return build_response({"status": "success"}, 200)
```
and that's it, your app should be good to go as far as CORs are concerned. I would
recommend only allowing requests from certain sites though instead of allowing
any origin to make a request to your function, that's going to be covered in [this](https://github.com/ipbrennan90/lambda-tutorial/tree/simple-security)
branch.
