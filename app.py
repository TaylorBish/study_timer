from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/flask'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    cars = db.relationship('Car', backref="user", lazy=True)

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(120), nullable=False)
    model = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)

##Create a user
@app.route('/users', methods=['POST'])
def create_user():
        data = request.json
        new_user = User(username=data['username'], email=data['email'], password=data['password'])
        db.session.add(new_user)
        db.session.commit()

        return {"message": "User created successfully"}

##Get all users
@app.route('/users', methods=['GET'])
def get_users():
        all_users = User.query.all()

        results = []

        for user in all_users:
            users = {
                "username": user.username,
                "email": user.email
            }
            results.append(users)
        return results

##Route for getting user by ID
@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    users = User.query.filter_by(id=int(user_id)).all()

    results = []

    for user in users:
        users = {
            "username": user.username,
            "email": user.email
        }
        results.append(users)
    return results

#Create a car
@app.route('/cars/<user_id>', methods=['POST'])
def create_car(user_id):
        data = request.json
        new_car = Car(make=data['make'], model=data['model'], user_id=int(user_id))
        db.session.add(new_car)
        db.session.commit()
        
        return jsonify(data)

##Get car by user id
@app.route('/cars/<user_id>', methods=['GET'])
def get_car(user_id):
        data = Car.query.filter_by(user_id=int(user_id)).all()

        results = []

        for car in data:
            cars = {
                "make": car.make,
                "model": car.model
            }
            results.append(cars)
        
        return results

