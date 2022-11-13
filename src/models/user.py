from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Relationships
    squads = db.relationship('Squad', back_populates='user', cascade='all, delete')

class UserSchema(ma.Schema):
    # Validation for name to be between 3-25 characters and only contain letters and spaces
    name = fields.String(validate=And(
        Length(min=3, max=25, error='Username must be between 3 and 25 characters long'),
        Regexp('^[a-zA-Z ]+$', error='Username can only contain letters and spaces')
    ))
    
    # Excludes user from squads field
    squads = fields.List(fields.Nested('SquadSchema', exclude=['user']))

    class Meta:
        fields = ('id', 'name', 'email', 'password', 'is_admin')
        ordered = True