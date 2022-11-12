from init import db, ma
from marshmallow import fields

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    squads = db.relationship('Squad', back_populates = 'users', cascade = 'all, delete')

class UserSchema(ma.Schema):
    squads = fields.List(fields.Nested('SquadSchema', exclude = ['users']))

    class Meta:
        fields = ('id', 'name', 'email', 'password', 'is_admin')