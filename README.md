# Hello-World with Zappa

## Install Python

If you don't already have it you'll need to install python, I recommend using homebrew

``` bash
brew update
brew install python 3
```

Always good to upgrade your essential packages

```bash
pip install --upgrade pip setuptools pipenv
```

We'll be using a Pipfile to manage dependencies, instantiate the pipfile and venv like this:

```bash
pipenv --three
pipenv shell
```

Should have a working virtual environment and pip file now.

Next, install zappa and flask, flask is a lightweight framework for python applications

```bash
pipenv install zappa flask
```

if you do not have the awscli installed:

```bash
pipenv install --dev awscli
```

this will help us get aws set up to play nicely with zappa

lets create the app file now

```bash
touch app.py
```

open it up in your favorite text editor

## app.py

```python
from flask import Flask

app = Flask(__name__)

# here is how we are handling routing with flask:
@app.route('/')
def index():
    return "Hello World!", 200

# include this for local dev

if __name__ == '__main__':
    app.run()
```

Now you have a tiny little app ready to go

now run it in the terminal:

```bash
export HELLO_WORLD = app.py
flask run

```
and check out your localhost at port 5000 and you should be welcomed by a little "Hello World!"


If you haven't already you'll need to configure your awscli by following these [amazon docs](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html)


## Deployment with Zappa

```bash
zappa init
```

this will create your zappa_settings.json file and add it to the project, now you can deploy!

this is what makes zappa so nice, it takes this tiny config and then packages and deploys with one command

you can check out more advanced settings to add into your project here: [advanced zappa settings](https://github.com/Miserlou/Zappa#advanced-settings)

```bash
zappa deploy
```

if you have any trouble with deploy on this one, such as seeing:

```json
{
    message: 'internal server error'
}
```
when you try to view your site, check cloudwatch, if your logs have something like:

```
Unable to import module 'handler': No module named builtins
```
there is most likely a difference between your local python version and pipenv's version
so double check that and re-deploy, using different versions on pipenv is as as easy as:

```bash
pipenv --two
```
and re-installing your dependencies on the new venv



this branch and my endeavours with zappa have been greatly aided by this [blog post](https://andrich.blog/2017/02/12/first-steps-with-aws-lambda-zappa-flask-and-python/) by [Oliver Andrich](https://andrich.blog)
