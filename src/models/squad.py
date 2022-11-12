from init import db, ma
from marshmallow import fields

class Squad(db.Model):
    __tablename__ = 'squads'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    league = db.Column(db.String)

    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='squads')


class SquadSchema(ma.Schema):
    users = fields.Nested('UserSchema', only=['name', 'email'])


    class Meta:
        fields = ('name', 'league', 'user')
        ordered = True