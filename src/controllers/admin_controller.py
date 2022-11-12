from flask import Blueprint
from init import db
from models.user import User, UserSchema
from controllers.auth_controller import authorize_user
from flask_jwt_extended import jwt_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/grant_admin/<int:user_id>/', methods=['PATCH'])
@jwt_required()
def grant_admin_access(user_id):
    # Admin can give a user admin privileges
    authorize_user()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)

    if user and user.is_admin is True:
        return {'Message': 'This user is an admin already.'}

    elif user:
        user.is_admin = True
        db.session.commit()
        return UserSchema(exclude=['password']).dump(user)

    else:
        return {'Message': f'User with id: {user_id} not found'}

@admin_bp.route('/remove_admin/<int:user_id>/', methods=['PATCH'])
@jwt_required()
def remove_admin_access(user_id):
    # Admin removes admin privileges from another admin
    authorize_user()

    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)

    if user and user.is_admin is False:
        return {'Message': 'This user is not an admin'}

    elif user:
        user.is_admin = False
        db.session.commit()
        return UserSchema(exclude=['password']).dump(user)

    else:
        return {'Message': f'User with id: {user_id} not found'}
