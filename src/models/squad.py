from init import db, ma
from marshmallow import fields

class Squad(db.Model):
    __tablename__ = 'squads'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    league = db.Column(db.String)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

    users = db.relationship('User', back_populates='squads')
    user_players = db.relationship('UserPlayer', back_populates='squads', cascade = 'all, delete')

class SquadSchema(ma.Schema):
    users = fields.Nested('UserSchema', only=['name', 'email'])
    user_players = fields.List(fields.Nested('UserPlayerSchema', exclude = ['squads']))

    class Meta:
        fields = ('name', 'league', 'users')
        ordered = True