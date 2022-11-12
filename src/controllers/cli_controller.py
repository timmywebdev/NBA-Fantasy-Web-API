from flask import Blueprint
from init import db, bcrypt
from models.squad import Squad
from models.user import User
from models.players import Player


db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_db():
    db.create_all()
    print("Tables created")

@db_commands.cli.command('drop')
def drop_db():
    db.drop_all()
    print("Tables dropped")

@db_commands.cli.command('seed')
def seed_db():
    users = [
        User(
            email = 'admin@nbafantasy.com',
            password = bcrypt.generate_password_hash('admin123').decode('utf-8'),
            is_admin = True
        ),
        User(
            name = 'Anthony Hoson',
            email = 'ahoson@abc.com',
            password = bcrypt.generate_password_hash('hello123').decode('utf-8')
        ),
        User(
            name = 'Matthew News',
            email = 'matthewnews@abc.com',
            password = bcrypt.generate_password_hash('password123').decode('utf-8')
        ),
        User(
            name = 'Timothy Newman',
            email = 'tnewman@abc.com',
            password = bcrypt.generate_password_hash('happy123').decode('utf-8')
        )
    ]

    db.session.add_all(users)
    db.session.commit()
    
    players = [
        Player(
            name = 'Stephen Curry',
            team = 'Golden State Warriors',
            position = 'PG',
            points = '40',
            rebounds = '5',
            assists = '5'

        ),
        Player(
            name = 'Lebron James',
            team = 'Los Angeles Lakers',
            position = 'SF',
            points = '15',
            rebounds = '10',
            assists = '10'
        ),
        Player(
            name = 'James Harden',
            team = 'Philadelphia 76ers',
            position = 'PG',
            points = '30',
            rebounds = '5',
            assists = '10'
        )
    ]

    db.session.add_all(players)
    db.session.commit()


    squads = [
        Squad(
            user = users[1],
            players = players[0]
        ),
        Squad(
            user = users[3],
            players = players[1]
        ),
        Squad(
            user = users[2],
            players = players[2]
        )
    ]

    db.session.add_all(squads)
    db.session.commit()
    print("Tables seeded")