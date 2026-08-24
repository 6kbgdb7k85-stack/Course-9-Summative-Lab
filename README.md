# Course-9-Summative-Lab

## Description
Flask SQLAlchemy Workout Application Backend

## Setup
- clone repo
- run pipenv install
- run pipenv shell
- navigate to directory /server and run the following
    - export FLASK_APP=app.py
    - export FLASK_RUN_PORT=5555
    - flask db upgrade head

## Usage
- navigate to server directory
- within pipenv environment (either through pipenv shell or pipenv run *command*) run python seed.py to seed the database with random data
    - data will be formatted like real entries, but will be nonsensical as workout and exercise data
- within pipenv environment run python app.py
- within pipenv environment run flask shell

## Using API endpoints in Flask Shell
- set a var such as "client" to represent the client making api calls
    - client = app.test_client()
- then use the following to make requests to the api
    - response = client.*method*(*api_endpoint*, json={*request_data*})
    - response.get_json() and response.status_code can be used afterwards to check response details

## Features/Endpoints
- /workouts
    - GET: return all existing workouts
    - POST: add new workout to database with the input data
- /workouts/:id
    - GET: return details of the workout and associated exercise and workout_exercise entries
    - DELETE: remove the indicated workout
- /exercises
    - GET: return all existing exercises
    - POST: add new exercise to database with the input data
- /exercises/:id
    - GET: return details of the exercise and associated workouts and workout_exercise entries
    - DELETE: remove the indicated exercise
- /workouts/:workout_id/exercises/:exercise_id/workout_exercises
    - POST: add indicated exercise to indicated workout
