## flask-bucketlist-api
[![Build Status](https://travis-ci.org/borenho/flask-bucketlist-api.svg)](https://travis-ci.org/borenho/flask-bucketlist-api)  [![Coverage Status](https://coveralls.io/repos/github/borenho/flask-bucketlist-api/badge.svg)](https://coveralls.io/github/borenho/flask-bucketlist-api)

A RESTful api built on Python Flask, with endpoints that:


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
| POST /bucketlists/<id>/items/      | TRUE            |
| PUT /bucketlists/<id>/items/<item_id>         | TRUE            |
| DELETE /bucketlists/<id>/items/<item_id>        | TRUE            |
  
  ## Features
  - Token based authentication
  - Searching based on the name using a GET parameter q
  - Pagination; users can specify the number of results they would like to have via a GET parameter limit
  
  ## Getting Started
  - Clone the repo and `cd` into the project directory
  - Install and create a virtualenv using this tutorial: https://medium.com/@BoreCollins/task-automation-on-linux-3cf68fe0b389?source=user_profile---------13----------------
  - Install the project dependencies with `pip install -r requirements.txt`
  - Create a `.env` file to store the environment variables, type in `touch .env`
  - Copy and paste the following to it:
  ```
  source my-virtualenv/bin/activate
  export FLASK_APP="run.py"
  export SECRET="a-very-random-string-that-should-not-be-human-readable,-just-kidding-"
  export APP_SETTINGS="development"
  export DATABASE_URL="postgresql://localhost/dev_db"
  ```
  
  - Once everything is running well, run the aplication with `python manage.py runserver`
  - Use *postman* to test the api endpoints
  
  ## Running the tests
  Just do `nosetests --rednose`
  And to check test coverage percentage, `nosetests --rednose --with-coverage`
  
  ## Authors
  - Kibet Ruto
  
  ## License

  This project is licensed under the MIT License - see the LICENSE.md file for details
  
  ## Acknowledgement
  - Andela
