from flask import Blueprint, request
from init import db
from models.players import Player, PlayerSchema
from models.user import User
from controllers.auth_controller import authorize_user
from flask_jwt_extended import jwt_required, get_jwt_identity


players_bp = Blueprint('players', __name__, url_prefix='/players')

# ~~~~~~~~~~~~~~~~~~~ PLAYERS ~~~~~~~~~~~~~~~~~~~~
# GET, POST, PUT, PATCH, DELETE

# Do not need to be a user to use GET route for players
@players_bp.route('/')
def get_all_players():
    stmt = db.select(Player).order_by(Player.id.asc())
    players = db.session.scalars(stmt)
    return PlayerSchema(many=True).dump(players)

# Get one player and their stats
@players_bp.route('/<int:id>/')
def get_one_player(id):
    stmt = db.select(Player).filter_by(id=id)
    players = db.session.scalar(stmt)

    if players:
        return PlayerSchema().dump(players)

    return {'Error': f'Player not found with id {id}'}, 404

# ADMIN adds a player to database
@players_bp.route('/', methods=['POST'])
@jwt_required()
def create_player():
    authorize_user()

    data = PlayerSchema().load(request.json, partial=True)

    stmt = db.select(User).filter_by(id=get_jwt_identity())
    user = db.session.scalar(stmt)

    if user:
        player = Player(
            name = data['name'],
            team = data['team'],
            position = data['position'],
            points = data['points'],
            rebounds = data['rebounds'],
            assists = data['assists'],
        )

        db.session.add(player)
        db.session.commit()

        return {
                'Message': 'Player added successfully',
                'Player': PlayerSchema().dump(player)
        }

    return {'Error': 'You must be logged in to add a player to the database'}, 404

# ADMIN updates a players information
@players_bp.route('/<int:id>/update/', methods=['PUT', 'PATCH'])
@jwt_required()
def update_player(id):
    authorize_user()
    stmt = db.select(Player).filter_by(id=id)
    player = db.session.scalar(stmt)

    data = PlayerSchema().load(request.json, partial=True)

    if player:
        player.name = data.get('name') or player.name
        player.team = data.get('team') or player.team
        player.position = data.get('position') or player.position
        player.points = data.get('points') or player.points
        player.rebounds = data.get('rebounds') or player.rebounds
        player.assists = data.get('assists') or player.assists
        db.session.commit()
        return {
            "Message": "Player updated successfully",
            "Player": PlayerSchema().dump(player)
        }
    return {'Error': f'Player not found with id: {id}'}, 404

# ADMIN deletes a player from the database
@players_bp.route('/<int:id>/', methods=['DELETE'])
@jwt_required()
def delete_player(id):
    authorize_user()
    stmt = db.select(Player).filter_by(id=id)
    player = db.session.scalar(stmt)

    if player:
        db.session.delete(player)
        db.session.commit()
        return {'Message': f'Player with id: {id} successfully deleted.'}

    return {'Error': f'Player not found with id: {id}'}, 404