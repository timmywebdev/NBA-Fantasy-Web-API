from flask import Blueprint, request, abort
from init import db, bcrypt
from datetime import timedelta
from models.user import User, UserSchema
from flask_jwt_extended import create_access_token, get_jwt_identity
from sqlalchemy.exc import IntegrityError

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register/', methods=['POST'])
def register_user():
    # Register a new user
    data = UserSchema().load(request.json)

    # If email doesn't exist already in database, create new user. Bcrypt will hash the password before it is stored
    try:
        user = User(
            name = data['name'],
            email = data['email'],
            password = bcrypt.generate_password_hash(data['password']).decode('utf-8')  
        )
        db.session.add(user)
        db.session.commit()
        return UserSchema(exclude=['password']).dump(user), 201

    except IntegrityError:
        return {'Error': F'{user.email} or {user.name} already in use'}, 409

@auth_bp.route('/login/', methods=['POST'])
def login_user():
    # Login for user with 1 day token expiry
    stmt = db.select(User).filter_by(email=request.json['email'])
    user = db.session.scalar(stmt)

    # If login is successful, then create access token with 1 day expiry
    if user and bcrypt.check_password_hash(user.password, request.json['password']):
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
        return {'email': user.email, 'token': token, 'is_admin': user.is_admin}

    # If either or both inputs are incorrect, print invalid email OR password
    return {'Error': 'Invalid email or password'}, 401

def authorize_user():
    # Checks if user is an admin
    stmt = db.select(User).filter_by(id=get_jwt_identity())
    user = db.session.scalar(stmt)

    # If not admin, display error
    if not user.is_admin:
        abort(401, description='You must be an administrator to do that')
    return True