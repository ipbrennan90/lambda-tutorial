# Integrating RDS with your Lambda function

## Building the database

we'll accomplish this through the cli

```bash
aws rds create-db-instance \
  --db-instance-identifier <db identifier, nothing special here> \
  --db-instance-class db.t2.micro \
  --engine MySQL \
  --allocated-storage 5 \
  --no-publicly-accessible \
  --db-name <Name you want to give your database> \
  --master-username <this is db specific so use w/e you want> \
  --master-user-password <same as above, some symbos won't be accepted> \
  --backup-retention-period 3
```

You should be seeing some output to the console showing your new db and
its configuration

## Setting Environment Variables

Zappa makes this pretty easy, I don't really like the idea of putting it into my
zappa_settigns.py file so I opted to use .env with the dotenv package instead,
lets add the dependencies we'll need and import them first

* Make sure you are not in your virtual env when installing dependencies *
```bash
pipenv install dotenv
```

boot your venv back up:

```bash
pipenv shell
```

and import

```
import os
import logging
from dotenv import load_dotenv, find_dotenv
```

alright in your env we'll need to add a couple variables to get things working
with the new DB, first create a .env file then add these:
```
DB_HOST=<address of your new db, you can get this from the aws rds console, it will be the endpoint value when you expand your db information>
DB_USERNAME=<username you set in the cli command>
DB_PASSWORD=<password you set in the cli command>
DB_NAME=<name you set in the cli command>
```

let's get those and set them to global variables in app.py:

```python
# first, load your env file, replacing the path here with your own if it differs
dotenv = Dotenv(os.path.join(os.path.dirname(__file__), ".env"))
# update environment just in case
os.environ.update(dotenv)
# set globals
RDS_HOST = os.environ.get("DB_HOST")
RDS_PORT = int(os.environ.get("DB_PORT", 3306))
NAME = os.environ.get("DB_USERNAME")
PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")

# we need to instantiate the logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
```

now let's create a connect function for connecting to our new database:

```python
def connect():
    try:
        cursor = pymysql.cursors.DictCursor
        conn = pymysql.connect(RDS_HOST, user=NAME, passwd=PASSWORD, db=DB_NAME, port=RDS_PORT, cursorclass=cursor, connect_timeout=5)
        logger.info("SUCCESS: connection to RDS successful")
        return(conn)
    except Exception as e:
        logger.exception("Database Connection Error")
```

and add the call to connect in our index function for testing purposes:

```python
@app.route('/')
def index():
    connect()
    return "Hello World!", 200

```


## AWS VPC Configuration

before we run this though, we'll need to create an IAM role capable of making this
connection through VPC

sign in [here](https://console.aws.amazon.com/iam/.)

Since we have deployed before, you should see the role zappa automatically
created for us. Should have "ZappaLambdaExecutionRole" at the very end of
the title, click on that role.

You should see something like this:

![Alt text](/../screenshots/screenshots/attach-policy.png?raw=true "Attach Policy")

click attach policy and inside the policy list select AWSLambdaVPCAccessExecutionRole:

![Alt text](/../screenshots/screenshots/select-policy.png?raw=true "Select Policy")

ok, now our role should be good to go for interacting with our RDS on the default vpc,
let's configure the Lambda so it can connect to the RDS instance

open up your lambda console by heading [here](https://console.aws.amazon.com/lambda/home)
open up the lambda function you've deployed already, and click into the configuration tab:

![Alt text](/../screenshots/screenshots/lambda-config.png?raw=true "Lambda Config")

for role, select choose existing role, for exiting role, enter in the name of
the role we just created, then open up the advanced settings dropdown:

![Alt text](/../screenshots/screenshots/lambda-advanced.png?raw=true "Lambda Advanced")

At this point I just selected my default VPC in VPC, added three of the associated
subnets, and added the default security group in security groups. This should give your
lambda function access to the VPC where your RDS instance lives, otherwise we
will just get timeouts when we try to write and read from the database.

Press save and test, the output is generally useless here but it shouldn't throw
any weird errors. Now deploy the app:

```bash
zappa update
```

and tail

```bash
zappa tail
```

you should see your log for a successful connection to the RDS instance, if not
you may want to go back over the amazon steps, or open an issue on this branch.

For this section of the tutorial I had a lot of help from [this](http://docs.aws.amazon.com/lambda/latest/dg/vpc-rds.html) aws tutorial
