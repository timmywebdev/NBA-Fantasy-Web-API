from flask import Blueprint
from init import db
from models.players import Player
from models.squad import Squad, SquadSchema
from models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity

squad_bp = Blueprint('squad', __name__, url_prefix='/squad')

# ~~~~~~~~~~~~~~~~~~~ SQUAD PLAYERS ~~~~~~~~~~~~~~~~~~~~
# GET, POST, DELETE routes

# Users can view other users squad but they can only edit their own squad

# View a user's squad
@squad_bp.route('/<int:user_id>/')
@jwt_required()
def get_user_squads(user_id):
    stmt = db.select(Squad).where(Squad.user_id == user_id)
    players = db.session.scalars(stmt)
    return {'message': f'Here is the squad for user_id:{user_id}!',
            'squad': SquadSchema(exclude=['user'], many=True).dump(players)}, 201

# View your own squad
@squad_bp.route('/')
@jwt_required()
def get_own_squad():
    user_id = get_jwt_identity()
    stmt = db.select(Squad).where(Squad.user_id == user_id)
    players = db.session.scalars(stmt)
    return {'message': 'Here is your squad!',
            'squad': SquadSchema(exclude=['user'], many=True).dump(players)}, 201

# Allows user to add a player to their squad list
@squad_bp.route('/add/<int:id>', methods=['POST'])
@jwt_required()
def add_player_to_squad(id):

    stmt = db.select(Player).filter_by(id=id)
    player = db.session.scalar(stmt)

    if player:
        squad = Squad(
            player_id = id,
            user_id = get_jwt_identity()
        )
        db.session.add(squad)
        db.session.commit()
        return {
            "Message": "Player successfully added to Squad",
            "Squad": SquadSchema(exclude=['user', 'id']).dump(squad)
        }

    return {'Error': f'Player not found with id {id}'}, 404

# Allows user to remove a player from their squad list
@squad_bp.route('/remove/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_player_from_squad(id):
    stmt = db.select(Squad).filter_by(id=id)
    squad_player = db.session.scalar(stmt)

    # if squad player exists and the user_id is authenticated, remove player from squad
    if squad_player and squad_player.user_id == int(get_jwt_identity()):
        db.session.delete(squad_player)
        db.session.commit()
        return {
            "Message": "Player successfully removed from Squad"
        }

    return {'Error': f'Player not found with id {id}'}, 404



# @squad_bp.route('/remove/<int:squad_id>', methods=['DELETE'])
# @jwt_required()
# def remove_player_from_squad(squad_id):
#     stmt = db.select(Squad).filter_by(id = squad_id)
#     squad_player = db.session.scalar(stmt)
#     if not squad_player:
#         return {'Error': f'Player not found with id {squad_id} in your squad'}, 404
#     if squad_player:
#         if Squad.user_id == int(get_jwt_identity()):
#             db.session.delete(squad_player)
#             db.session.commit()
#             return {'Message': f'You have removed the player with id {squad_id} from your squad.'}

