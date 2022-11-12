from init import db, ma
from marshmallow import fields

class Squad(db.Model):
    __tablename__ = 'squads'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    league = db.Column(db.String)

    player_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    player = db.relationship('Player', back_populates='squads')
    user = db.relationship('User', back_populates='squads')


class SquadSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['name', 'email'])
    player = fields.Nested('PlayerSchema', exclude=['user'])

    class Meta:
        fields = ('name', 'league', 'user')
        ordered = True