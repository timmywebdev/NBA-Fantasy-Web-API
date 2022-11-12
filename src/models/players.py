from init import db, ma
from marshmallow import fields

class Player(db.Model):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    team = db.Column(db.String)
    position = db.Column(db.String)
    points = db.Column(db.Integer)
    rebounds = db.Column(db.Integer)
    assists = db.Column(db.Integer)

    # Relationships
    squads = db.relationship('Squad', back_populates='players', cascade='all, delete')


class PlayerSchema(ma.Schema):
    squads = fields.Nested('SquadSchema')

    class Meta:
        fields = ('id', 'name', 'team', 'position', 'points', 'rebounds', 'assists')
        ordered = True