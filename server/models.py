from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from marshmallow import Schema, fields
db = SQLAlchemy()

class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    category = db.Column(db.String)
    equipment_needed = db.Column(db.Boolean)

    workout_exercises = db.relationship("WorkoutExercise", back_populates="exercise")
    workouts = association_proxy("workout_exercises", "workout", creator=lambda workout_obj: Workout(workout=workout_obj))

    __tableargs__ = (
        db.CheckConstraint('name or category', name="req_name_or_category"),
    )

class ExerciseSchema(Schema):
    id = fields.Int()
    name = fields.String()
    category = fields.String()
    equipment_needed = fields.Bool()
    workouts = fields.List(fields.Nested(lambda: WorkoutSchema(exclude=("exercises",))))
    workout_exercises = fields.List(fields.Nested(lambda: WorkoutExerciseSchema(exclude=("workout","exercise"))))

class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer)
    notes = db.Column(db.Text(250))

    workout_exercises = db.relationship("WorkoutExercise", back_populates="workout")
    exercises = association_proxy("workout_exercises", "exercise", creator=lambda exercise_obj: Exercise(exercise=exercise_obj))

class WorkoutSchema(Schema):
    id = fields.Int()
    date = fields.Date()
    duration_minutes = fields.Int()
    notes = fields.String()
    exercises = fields.List(fields.Nested(lambda: ExerciseSchema(exclude=("workouts",))))
    workout_exercises = fields.List(fields.Nested(lambda: WorkoutExerciseSchema(exclude=("workout","exercise"))))

class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout = db.relationship("Workout", back_populates="workout_exercises")
    exercise = db.relationship("Exercise", back_populates="workout_exercises")

    __tableargs__ = (
        db.CheckConstraint('reps or sets', name="req_reps_or_sets")
    )

class WorkoutExerciseSchema(Schema):
    id = fields.Int()
    reps = fields.Int()
    sets = fields.Int()
    duration_seconds = fields.Int()
    workout = fields.Nested(lambda: WorkoutSchema(exclude=("workout_exercise", "exercises")))
    exercise = fields.Nested(lambda: ExerciseSchema(exclude=("workout_exercise", "workouts")))