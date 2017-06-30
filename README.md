# Hello-World with Zappa

## Install Python

If you don't already have it you'll need to install python, I recommend using homebrew

``` bash
brew update
brew install python 3
```

Always good to upgrade your essential packages

```
pip install --upgrade pip setuptools pipenv
```

We'll be using a Pipfile to manage dependencies, instantiate the pipfile and venv like this:

```
pipenv --three
pipenv shell
```

Should have a working virtual environment and pip file now.

Next, install zappa and flask, flask is a lightweight framework for python applications

```
pipenv install zappa flask
```

if you do not have the awscli installed:

```
pipenv install --dev awscli
```

this will help us get aws set up to play nicely with zappa

lets create the app file now

```
touch app.py
```

open it up in your favorite text editor

## app.py

```
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

```
export HELLO_WORLD = app.py
flask run

```
and check out your localhost at port 5000 and you should be welcomed by a little "Hello World!"
