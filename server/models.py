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

class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer)
    notes = db.Column(db.Text(250))

    workout_exercises = db.relationship("WorkoutExercise", back_populates="workout")
    exercises = association_proxy("workout_exercises", "exercise", creator=lambda exercise_obj: Exercise(exercise=exercise_obj))

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