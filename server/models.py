from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from marshmallow import Schema, fields, post_load, ValidationError, validates_schema
db = SQLAlchemy()

class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    category = db.Column(db.String)
    equipment_needed = db.Column(db.Boolean)

    workout_exercises = db.relationship("WorkoutExercise", back_populates="exercise", cascade="all, delete-orphan")
    workouts = association_proxy("workout_exercises", "workout", creator=lambda workout_obj: Workout(workout=workout_obj))

    __table_args__ = (
        db.CheckConstraint("NOT (name IS NULL AND category IS NULL)", name="req_name_or_category"),
    )

class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String()
    category = fields.String()
    equipment_needed = fields.Bool()
    workouts = fields.List(fields.Nested(lambda: WorkoutSchema(exclude=("exercises",))))
    workout_exercises = fields.List(fields.Nested(lambda: WorkoutExerciseSchema(exclude=("workout","exercise"))))

    @validates_schema
    def validate_name_or_category(self, data, **kwargs):
        if not data.get("name") and not data.get("category"):
            raise ValidationError("Exercise must have a name or category")

    @post_load
    def make_Exercise(self, data, **kwargs):
        return Exercise(**data)

class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer)
    notes = db.Column(db.Text(250))

    workout_exercises = db.relationship("WorkoutExercise", back_populates="workout", cascade="all, delete-orphan")
    exercises = association_proxy("workout_exercises", "exercise", creator=lambda exercise_obj: Exercise(exercise=exercise_obj))

    @validates('duration_minutes')
    def validate_duration_minutes(self,key,duration_minutes):
        if duration_minutes and duration_minutes < 0:
            raise ValueError("duration_minutes cannot be negative")
        return duration_minutes

class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date()
    duration_minutes = fields.Int()
    notes = fields.String()
    exercises = fields.List(fields.Nested(lambda: ExerciseSchema(exclude=("workouts",))))
    workout_exercises = fields.List(fields.Nested(lambda: WorkoutExerciseSchema(exclude=("workout","exercise"))))

    @validates_schema
    def validate_duration_minutes(self, data, **kwargs):
        if data.get("duration_minutes") and data.get("duration_minutes") < 0:
            raise ValidationError("Duration must be greater than 0")

    @post_load
    def make_workout(self, data, **kwargs):
        return Workout(**data)

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

    @validates('duration_seconds')
    def validate_duration_seconds(self, key, duration_seconds):
        if duration_seconds < 0:
            raise ValueError("duration_seconds cannot be negative")
        return duration_seconds

    __table_args__ = (
        db.CheckConstraint(reps.is_not(None) | sets.is_not(None), name="req_reps_or_sets"),
    )

class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    reps = fields.Int()
    sets = fields.Int()
    exercise_id = fields.Int()
    workout_id = fields.Int()
    duration_seconds = fields.Int()
    workout = fields.Nested(lambda: WorkoutSchema(exclude=("workout_exercises", "exercises")), dump_only=True)
    exercise = fields.Nested(lambda: ExerciseSchema(exclude=("workout_exercises", "workouts")), dump_only=True)

    @validates_schema
    def validate_duration_seconds(self, data, **kwargs):
        if data.get("duration_seconds") and data.get("duration_seconds") < 0:
            raise ValidationError("Duration must be greater than 0")
    @validates_schema
    def validate_reps_or_sets(self,data,**kwargs):
        if not data.get("reps") and not data.get("sets"):
            raise ValidationError("Must have at least one of [\"sets\",\"reps\"]")


    @post_load
    def make_exercise_workout(self, data, **kwargs):
        return WorkoutExercise(**data)