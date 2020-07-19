
# Capstone Project
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

The app allows one to: 

1) Display actors and movies.
2) Add new actors and movies.
3) Update existing actors details.
4) Update existing movies details.
5) Delete specific actor from database.
6) Delete specific movie from database.

- Roles:
  - Casting Assistant
    - Can view actors and movies

  - Casting Director
    - All permissions a Casting Assistant has and…
    - Add or delete an actor from the database
    - Modify actors or movies

  - Executive Producer
    - All permissions a Casting Director has and…
    - Add or delete a movie from the database

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

Working within a virtual environment is recommended.

#### PIP Dependencies

navigate to the `/capstone` directory and run:

```bash
pip install -r requirements.txt
```

This will install all of the required packages in the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup for postman collection tests execution
With Postgres running, restore a database using the casting.psql file provided. From the capstone folder in terminal run:

```bash
dropdb casting
createdb casting
psql casting < casting.psql
```
Omit the dropdb command the first time you run.

## Running the server locally

From within the `capstone` directory

To run the server, execute:

```bash
python app.py
```

Import capstone.postman_collection.json in postman which is provided in capstone folder

In this collection, tokens are already provided in authorization header according to role.
so permissions are also getting tested for each role.

By clicking on runner in postman, you can execute test cases of given collection which contains all the api.

## Testing
To run the tests, run
```
dropdb casting
createdb casting
psql casting < casting.psql
python test_app.py
```
Omit the dropdb command the first time you run tests.
Second time onwards, run all commands in given sequence.

## Database Setup for flask migration

After checking postman collection and doing testing through unittest, run
```bash
dropdb casting
createdb casting
```

Here, run following commands to replicate sqlalchemy schema models to database.
```bash
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

After successfully created table in db, run flask server
```bash
python app.py
```

## API Reference

### Getting Started

* Capstone Base URL: `http://127.0.0.1:5000/`
* Heroku hosted URL: `https://casting-agency-rt.herokuapp.com/`
* Authentication: Authentication or API keys are provided in .env file.

### Error Handling

Errors are returned in the following json format:

```json
      {
      "success":false,
      "error": 404,
      "message":"Resource not found"
      }
```

The error codes currently returned are:

* 400 – bad request
* 404 – resource not found
* 422 – unprocessable
* 500 – internal server error
* 401 – unauthorized


### Endpoints

#### GET /actors

- General: 
  - Returns all the actors.

- Sample:  `{{host}}/actors`

```json
{
  "actors": [
    {
      "age": 36,
      "gender": "Male",
      "id": 1,
      "name": "Caprio"
    },
    {
      "age": 45,
      "gender": "Male",
      "id": 2,
      "name": "SK"
    },
    {
      "age": 29,
      "gender": "Male",
      "id": 3,
      "name": "Shahid"
    },
    {
      "age": 24,
      "gender": "Male",
      "id": 4,
      "name": "Rock"
    },
    {
      "age": 36,
      "gender": "Female",
      "id": 5,
      "name": "Kareena"
    },
    {
      "age": 26,
      "gender": "Female",
      "id": 6,
      "name": "Alia"
    }
  ],
  "success": true
}
```

#### GET /movies
- General:
  - Returns all movies

- Sample: `{{host}}/movies`<br>

```json
{
  "movies": [
    {
      "id": 1,
      "release_date": "Wed, 30 May 2018 00:00:00 GMT",
      "title": "KGF"
    },
    {
      "id": 2,
      "release_date": "Mon, 12 Sep 2016 00:00:00 GMT",
      "title": "PK"
    },
    {
      "id": 3,
      "release_date": "Sat, 17 Mar 2012 00:00:00 GMT",
      "title": "Dhoom"
    },
    {
      "id": 4,
      "release_date": "Fri, 22 Jul 2011 00:00:00 GMT",
      "title": "Inception"
    },
    {
      "id": 5,
      "release_date": "Fri, 20 Mar 2015 00:00:00 GMT",
      "title": "Interstellar"
    }
  ],
  "success": true
}
```


#### POST /actors

- General:
  - Creates a new actor.

- Sample input: `{{host}}/actors`
```json
{
    "name": "rohit",
    "age": 23,
    "gender": "Male"
}
```
- Output:
```json
{
  "actor": {
    "age": 23,
    "gender": "Male",
    "id": 7,
    "name": "rohit"
  },
  "success": true
}
```

#### POST /movies

- General:
  - Creates a new movie.

- Sample input: `{{host}}/movies`
```json
{
    "title": "Dil Bechara",
    "release_date": "2020-07-22"
}
```
- Output:
```json
{
  "movie": {
    "id": 6,
    "release_date": "Wed, 22 Jul 2020 00:00:00 GMT",
    "title": "Dil Bechara"
  },
  "success": true
}
```

#### PATCH /actors/<id>

- General:
  - Update given details of given actor

- Sample Input: `{{host}}/actors/2`
```json
{
    "age": 36
}
```

```json
{
  "actor": {
    "age": 36,
    "gender": "Male",
    "id": 2,
    "name": "SK"
  },
  "success": true
}
```

#### PATCH /movies/<id>

- General:
  - Update given details of given movie

- Sample Input: `{{host}}/movies/2`
```json
{
    "title": "Untold story"
}
```

```json
{
  "movie": {
    "id": 2,
    "release_date": "Mon, 12 Sep 2016 00:00:00 GMT",
    "title": "Untold story"
  },
  "success": true
}
```

#### DELETE /actors/<id>

- General:
  - Delete given actor

- Sample: `{{host}}/actors/2`

```json
{
  "delete": 2,
  "success": true
}
```

#### DELETE /movies/<id>

- General:
  - Delete given movie

- Sample: `{{host}}/movies/2`

```json
{
  "delete": 2,
  "success": true
}
```

## Authors
- Rohit Tidke created these APIs and test suite to integrate with the frontend and this README.
