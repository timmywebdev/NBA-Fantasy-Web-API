from init import db, ma
from marshmallow import fields

class Squad(db.Model):
    __tablename__ = 'squads'

    id = db.Column(db.Integer, primary_key=True)

    # Foreign Keys
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationships
    players = db.relationship('Player', back_populates='squads')
    user = db.relationship('User', back_populates='squads')


class SquadSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['name'])
    players = fields.Nested('PlayerSchema', only=['name'])

    class Meta:
        fields = ('id', 'user', 'players')
        ordered = True