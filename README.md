# Lambda Tutorial

I built this tutorial on lambda because of my original struggles getting lambda set up and working. this covers:

* set up with zappa
* vpc to connect to a mysql RDS instance on amazon
* RDS persistence and querying through the lambda function
* CORs setup
* simple security

The tutorial should be done by checking out these branches and going through the readmes in this order

* hello-world
* routing
* rds-integration
* database-requests

If you just want to run the app, adjust your .env to have the values for the
config vars in .env.example and run:

```bash
pipenv install

```

then,

```
zappa deploy
```

if you get stuck here I'd recommend at least running through the readme in the [rds-integration](https://github.com/ipbrennan90/lambda-tutorial/tree/rds-integration) branch



I have done my best to keep this simple and short, please open any issues if you have trouble with an explanation or get stuck on a step and I will work hard to solve those.
