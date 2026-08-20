#!/usr/bin/env python3
import random
from datetime import date

from faker import Faker

from app import app
from models import *

fake = Faker()

with app.app_context():

    Exercise.query.delete()
    Workout.query.delete()
    WorkoutExercise.query.delete()

    exercises = []
    for i in range(10):
        e = Exercise(name=fake.word(),category=fake.word(),equipment_needed=bool(random.getrandbits(1)))
        exercises.append(e)
    db.session.add_all(exercises)
    db.session.commit()

    workouts = []
    for i in range(10):
        w = Workout(date=date.fromisoformat(fake.date()), duration_minutes=random.randint(1,60),notes=fake.paragraph())
        workouts.append(w)
    db.session.add_all(workouts)
    db.session.commit()

    workout_exercises = []
    for i in range(10):
        db.session.add(WorkoutExercise(workout=random.choice(workouts), exercise=random.choice(exercises), reps=random.randint(1,10), sets=random.randint(10,10), duration_seconds=random.randint(1,60)))

    db.session.commit()