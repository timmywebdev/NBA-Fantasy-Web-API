from flask import Blueprint, request
from init import db
from models.players import Player
from models.squad import Squad, SquadSchema
from models.user import User
from controllers.auth_controller import authorize_user
from flask_jwt_extended import jwt_required, get_jwt_identity

squad_bp = Blueprint('squad', __name__, url_prefix='/squad')

# Squads
# GET, POST, DELETE routes for Squads
# Users can view other users squads but they can only edit their own squad

# View a user's squad
@squad_bp.route('/to_do/<int:user_id>/')
@jwt_required()
def get_user_squads(user_id):
    stmt = db.select(Squad).where(and_(
        Squad.user_id == user_id,
        Squad.tag == 'To Do'
    ))
    players = db.session.scalars(stmt)

    return SquadSchema(many=True).dump(players)

# Allows user to add a player to their squad
@squad_bp.route('/to_do/<int:id>/', methods=['POST'])
@jwt_required()
def add_player_to_squad(id):
    stmt = db.select(Player).filter_by(id=id)
    player = db.session.scalar(stmt)

    if player:
        squad = Squad(
            squad_id = id,
            name = (),
            league = 'To Do',
            player_id = id
            user_id = get_jwt_identity()
        )
        db.session.add(squad)
        db.session.commit()
        return {
            "Message": "Player successfully added to Squad",
            "Entry": SquadSchema().dump(squad)
        }

    return {'Error': f'Player not found with id {id}'}, 404

# Allows user to remove a player from their squad

