# flask-bucketlist-api
[![Build Status](https://travis-ci.org/borenho/flask-bucketlist-api.svg?branch=master)](https://travis-ci.org/borenho/flask-bucketlist-api?branch=master)  [![Coverage Status](https://coveralls.io/repos/github/borenho/flask-bucketlist-api/badge.svg?branch=master)](https://coveralls.io/github/borenho/flask-bucketlist-api?branch=master)

A RESTFUL bucketlist api built on Python Flask that allows users to keep track of the things they want to achieve and experience before reaching a certain age, and to share the fun with others along the way.

# Prerequisites

To run the app, you need to install a couple of dependencies. Check the `requirements.txt` file to see the dependencies. I will guide you on the installation part below.

# Features
The api has endpoints that:


a.) Enable users to create accounts and login into the application

| EndPoint                 | Public Access   |
| ------------------------ |:---------------:|
| POST /auth/register      | TRUE            |
| POST /auth/login         | TRUE            |
| POST /auth/logout        | TRUE            |
| POST /auth/reset-password| TRUE            |


b.) Enable users to create, update, view and delete a bucket list

| EndPoint                 | Public Access   |
| ------------------------ |:---------------:|
| POST /bucketlists/      | FALSE            |
| GET /bucketlists/         | FALSE            |
| GET /bucketlists/<id>    | FALSE
| PUT /bucketlists/<id>        | FALSE            |
| DELETE /bucketlists/<id>| FALSE            |


c.) Add, update, view or delete items in a bucket list

| EndPoint                 | Public Access   |
| ------------------------ |:---------------:|
| POST /bucketlists/<id>/items/      | FALSE            |
| PUT /bucketlists/<id>/items/<item_id>         | FALSE            |
| DELETE /bucketlists/<id>/items/<item_id>        | FALSE            |
  
  ## Other Features
  - Token based authentication
  - Searching based on the name using a GET parameter q
  - Pagination; users can specify the number of results they would like to have via a GET parameter limit
  
  # Installation
  - You need to have Python installed to run the application. I also use postgres database.

  - Use this simple tutorial I wrote to set it up within minutes - https://medium.com/@BoreCollins/task-automation-on-linux-3cf68fe0b389

  - Remember to also set up virtualenv and virtualenvwrapper to manage the dependencies (the tutorial shall guide you)

  - Now clone the repo to get a copy of the working directory on your local machine.

  - Fire up your terminal/cmd and paste the following command: git clone https://github.com/borenho/flask-bucketlist-api.git and press Enter
  - `cd` into the project directory, like `cd flask-bucketlist-api` and press enter

  - Once you're done, install all the requirements with the following command (paste it on your terminal) `pip install -r requirements.txt`
  
  ## Env variables
  - Create a `.env` file to store the environment variables, type in `touch .env`
  
  - Copy and paste the following to it:
  ```
  source my-virtualenv/bin/activate
  export FLASK_APP="run.py"
  export SECRET="a-very-random-string-that-should-not-be-human-readable,-just-kidding-"
  export APP_SETTINGS="development"
  export DATABASE_URL="postgresql://localhost/dev_db"
  ```
  
  ## Running the application
  - Once everything is running well, activate the virtualenv with `source .env` 
  - Now run the aplication with `python manage.py runserver`
  - Use *postman* to test the api endpoints
  
  # Running the tests
  - In your terminal within the project directory, run `nosetests --rednose`
  - And to check test coverage percentage run `nosetests --rednose --with-coverage`
  
  # Authors
  - Kibet Ruto
