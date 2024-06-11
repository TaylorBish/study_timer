from flask import Blueprint, request
from study_timer.extensions import db
from study_timer.models.user import User

user_route = Blueprint('user_route', __name__)


@user_route.route('/users', methods=['POST'])
def create_user():
        data = request.json
        new_user = User(username=data['username'], email=data['email'], password=data['password'])
        db.session.add(new_user)
        db.session.commit()

        return {"message": "User created successfully"}

##Get all users
@user_route.route('/users', methods=['GET'])
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
@user_route.route('/users/<user_id>', methods=['GET'])
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