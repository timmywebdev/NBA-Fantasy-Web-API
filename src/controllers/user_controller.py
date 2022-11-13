from flask import Blueprint, request
from init import db, bcrypt
from models.user import User, UserSchema
from controllers.auth_controller import authorize_user
from flask_jwt_extended import get_jwt_identity, jwt_required

users_bp = Blueprint('users', __name__, url_prefix='/users')

# ~~~~~~~~~~~~~~~~~~~ USERS ~~~~~~~~~~~~~~~~~~~~
# GET, POST, PUT, PATCH, DELETE routes

# Get list of all users (ADMIN ONLY)
@users_bp.route('/')
@jwt_required()
def get_all_users():
    authorize_user()
    stmt = db.select(User).order_by(User.id)
    users = db.session.scalars(stmt)
    return UserSchema(many=True, exclude=['password']).dump(users)

# Get one singular user and their squad (Login ONLY)
@users_bp.route('/<int:id>/')
@jwt_required()
def get_one_user(id):
    # Allows a user to get another user details
    stmt = db.select(User).filter_by(id=id)
    user = db.session.scalar(stmt)

    if user:
        return UserSchema(exclude=['password', 'email']).dump(user)

    return {'error': f'User not found with id {id}'}, 404

#  Update user information (Only that user can change)
@users_bp.route('/update/', methods=['PUT', 'PATCH'])
@jwt_required()
def update_user():
    # User update their name, password or email
    stmt = db.select(User).filter_by(id=get_jwt_identity())
    user = db.session.scalar(stmt)

    data =  UserSchema().load(request.json, partial=True)

    if user:
        user.name = data.get('name') or user.name
        user.email = data.get('email') or user.email
        if data.get('password'):
            user.password = bcrypt.generate_password_hash(request.json.get('password')).decode('utf-8')
        db.session.commit()
        return {
            "Message": f"User successfully updated",
            "User": UserSchema(exclude=['password']).dump(user)
        }
    return {'error': f'User not found with id {id}'}, 404