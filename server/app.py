from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
from marshmallow import ValidationError

from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

#get workouts or add new workout
@app.route("/workouts", methods=["GET","POST"])
def manage_workouts():
    if request.method == "GET":
        workouts = Workout.query.all()
        response_body = WorkoutSchema(many=True).dump(workouts)
        return make_response(response_body, 200)
    elif request.method == "POST":
        #handle schema validation
        try:
            new_workout = WorkoutSchema().load(request.get_json())
        except ValidationError as e:
            return make_response({"error":e.messages}, 400)
        db.session.add(new_workout)
        #try except for any errors the schema didn't/couldn't check
        try:
            db.session.commit()
            response_body = WorkoutSchema().dump(new_workout)
            status = 201
        except:
            response_body = {"error": "Internal server error"}
            status = 500
        return make_response(response_body, status)

#get or delete workout by id
@app.route("/workouts/<int:id>", methods=["GET","DELETE"])
def manage_workout_by_id(id):
    workout = Workout.query.get(id)
    #make sure workout is found before working with it
    if not workout:
        return make_response({"error": f"Workout {id} not found"}, 404)
    if request.method == "GET":
        response_body = WorkoutSchema().dump(workout)
        status = 200
        return make_response(response_body, status)
    elif request.method == "DELETE":
        #handle any errors from attempting to delete
        try:
            db.session.delete(workout)
            db.session.commit()
            return "Workout deleted",204
        except:
            return make_response({"error":"Internal server error"}, 500)

#get exercises or add new exercise
@app.route("/exercises",methods=["GET","POST"])
def manage_exercises():
    if request.method == "GET":
        exercises = Exercise.query.all()
        response_body = ExerciseSchema(many=True).dump(exercises)
        return make_response(response_body, 200)
    elif request.method == "POST":
        #handle schema validation
        try:
            new_exercise = ExerciseSchema().load(request.get_json())
        except ValidationError as e:
            return make_response({"error":e.messages}, 400)
        db.session.add(new_exercise)
        #try except for any errors the schema didn't/couldn't check
        try:
            db.session.commit()
            response_body = ExerciseSchema().dump(new_exercise)
            status = 201
        except:
            response_body = {"error": "Internal server error"}
            status = 500
        return make_response(response_body, status)

#get or delete exercise by id
@app.route("/exercises/<int:id>",methods=["GET","DELETE"])
def manage_exercise_by_id(id):
    exercise = Exercise.query.get(id)
    #ensure exercise exists before attempting to work with it
    if not exercise:
        return make_response({"error":f"Exercise {id} not found"}, 404)
    if request.method == "GET":
        response_body = ExerciseSchema().dump(exercise)
        return make_response(response_body, 200)
    elif request.method == "DELETE":
        #handle any errors from attempting to delete
        try:
            db.session.delete(exercise)
            db.session.commit()
            return "Exercise deleted", 204
        except:
            return make_response({"error":"Internal server error"}, 500)

#add exercise to workout
@app.route("/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises", methods=["POST"])
def add_exercise_to_workout(workout_id, exercise_id):
    exercise = Exercise.query.get(exercise_id)
    workout = Workout.query.get(workout_id)
    request_data = request.get_json()
    #ensure exercise and workout exist before attempting to join them
    if not exercise or not workout:
        return make_response({"error":f"Workout {workout_id} and/or Exercise {exercise_id} not found"}, 404)
    #handle schema validations
    try:
        new_workout_exercise = WorkoutExerciseSchema().load({"exercise_id":exercise.id, "workout_id":workout.id, **request_data})
    except ValidationError as e:
        return make_response({"errors":e.messages},400)
    #try except for any errors the schema didn't/couldn't check
    try:
        db.session.add(new_workout_exercise)
        db.session.commit()
        response_body = WorkoutExerciseSchema().dump(new_workout_exercise)
        status = 201
    except:
        response_body = {"error":"internal server error"}
        status = 500
    return make_response(response_body, status)

if __name__ == '__main__':
    app.run(port=5555, debug=True)