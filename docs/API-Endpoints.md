# API Endpoints Documentaiton

## Table Of Contents

- [Auth Routes](#auth-routes)
- [Admin Routes](#admin-routes)
- [User Routes](#user-routes)
- [Player Routes](#player-routes)
- [Squad Routes](#squad-routes)

### Auth Routes

#### **Route: /auth/register/**

- Request Verb: POST
- Function: Registers a new user in the database
- Required Arguments: N/A
- Authentication: N/A
- Authorization: N/A
- Example Request: 
```JSON
{
"name": "Johnny",
"email": "jbravo80@CN.com",
"password": "handsome"
}
```
- Example Response:
```JSON
{
    "message": "You are now registered!",
    "user": {
        "id": 6,
        "name": "Johnny",
        "email": "jbravo80@CN.com",
        "is_admin": false
    }
}
```

#### **Route: /auth/login/**

- Request Verb: POST
- Function: Registered user login
- Required Arguments: N/A
- Authentication: N/A
- Authorization: N/A
- Example Request: 
```JSON
{
    "email": "admin@nbafantasy.com",
    "password": "admin123"
}
```
- Example Response:
```JSON
{
    "email": "admin@nbafantasy.com",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2ODMzNzA3MCwianRpIjoiZjcyNGQ1NjctN2ZkZi00OWE1LWEzNjQtZTdiMTk4NDMyZWIxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE2NjgzMzcwNzAsImV4cCI6MTY2ODQyMzQ3MH0.IWFaPc6x9io8mQEurF98ZEHa9ESXtF1_taAViBoAqqA",
    "is_admin": true
}
```

### Admin Routes

#### **Route: /admin/give_admin/\<int:user_id>/**

- Request Verb: PATCH
- Function: Gives admin privileges to a user
- Required Arguments: user_id
- Authentication: jwt_required
- Authorization: Admin only - get_jwt_identity
- Example Request: N/A
- Example Response:
```JSON
{
    "message": "You have successfully given admin privileges to this user!",
    "user": {
        "id": 2,
        "name": "Anthony Hoson",
        "email": "ahoson@abc.com",
        "is_admin": true
    }
}
```

#### **Route: /admin/remove_admin/\<int:user_id>/**

- Request Verb: PATCH
- Function: Removes admin privileges from a user
- Required Arguments: user_id
- Authentication: jwt_required
- Authorization: Admin only - get_jwt_identity
- Example Request: N/A
- Example Response:
```JSON
{
    "message": "You have successfully removed admin privileges from this user!",
    "user": {
        "id": 2,
        "name": "Anthony Hoson",
        "email": "ahoson@abc.com",
        "is_admin": false
    }
}
```

### User Routes

#### **Route: /users/**

- Request Verb: GET
- Function: Returns all users
- Required Arguments: N/A
- Authentication: jwt_required
- Authorization: Admin only - get_jwt_identity
- Example Request: N/A
- Example Response:
```JSON
[
    {
        "id": 1,
        "name": null,
        "email": "admin@nbafantasy.com",
        "is_admin": true
    },
    {
        "id": 2,
        "name": "Anthony Hoson",
        "email": "ahoson@abc.com",
        "is_admin": false
    },
    {
        "id": 3,
        "name": "Matthew News",
        "email": "matthewnews@abc.com",
        "is_admin": false
    },
    {
        "id": 4,
        "name": "Timothy Newman",
        "email": "tnewman@abc.com",
        "is_admin": false
    }
]
```

#### **Route: /users/\<int:id>/**

- Request Verb: GET
- Function: Returns one user
- Required Arguments: id
- Authentication: jwt_required
- Authorization: N/A
- Example Request: N/A
- Example Response:
```JSON
{
    "id": 4,
    "name": "Timothy Newman",
    "is_admin": false
}
```

#### **Route: /users/update/**

- Request Verb: PUT, PATCH
- Function: Updates a user's own username, email and/or password
- Required Arguments: N/A
- Authentication: jwt_required
- Authorization: N/A
- Example Request:
```JSON
{
    "name": "Johnny Bravo"
}
```
- Example Response:
```JSON
{
    "Message": "User successfully updated",
    "User": {
        "id": 2,
        "name": "Johnny Bravo",
        "email": "ahoson@abc.com",
        "is_admin": false
    }
}
```

### Player Routes

#### **Route: /players/**

- Request Verb: GET
- Function: Returns all players
- Required Arguments: N/A
- Authentication: N/A
- Authorization: N/A
- Example Request: N/A
- Example Response:
```JSON
[
    {
        "id": 1,
        "name": "Stephen Curry",
        "team": "Golden State Warriors",
        "position": "PG",
        "points": 40,
        "rebounds": 5,
        "assists": 5
    },
    {
        "id": 2,
        "name": "Lebron James",
        "team": "Los Angeles Lakers",
        "position": "SF",
        "points": 15,
        "rebounds": 10,
        "assists": 10
    },
    {
        "id": 3,
        "name": "James Harden",
        "team": "Philadelphia 76ers",
        "position": "PG",
        "points": 30,
        "rebounds": 5,
        "assists": 10
    }
]
```

#### **Route: /players/\<int:id>/**

- Request Verb: GET
- Function: Returns one player
- Required Arguments: id
- Authentication: N/A
- Authorization: N/A
- Example Request: N/A
- Example Response:
```JSON
{
    "id": 2,
    "name": "Lebron James",
    "team": "Los Angeles Lakers",
    "position": "SF",
    "points": 15,
    "rebounds": 10,
    "assists": 10
}
```

#### **Route: /players/**

- Request Verb: POST
- Function: Creates a new player in the database
- Required Arguments: N/A
- Authentication: jwt_required
- Authorization: Admin only - get_jwt_identity
- Example Request:
```JSON
{
    "name": "Timothy Nguyen",
    "team": "Golden State Warriors",
    "position": "Small Forward",
    "points": "100",
    "rebounds": "50",
    "assists": "1"
}
```
- Example Response:
```JSON
{
    "Message": "Player added successfully",
    "Player": {
        "id": 4,
        "name": "Timothy Nguyen",
        "team": "Golden State Warriors",
        "position": "Small Forward",
        "points": 100,
        "rebounds": 50,
        "assists": 1
    }
}
```

#### **Route: /players/\<int:id>/update/**

- Request Verb: PUT, PATCH
- Function: Updates an existing player in the database
- Required Arguments: id
- Authentication: jwt_required
- Authorization: Admin only - get_jwt_identity
- Example Request:
```JSON
{
    "points": "20",
    "rebounds": "50",
    "assists": "1"
}
```
- Example Response:
```JSON
{
    "Message": "Player updated successfully",
    "Player": {
        "id": 4,
        "name": "Timothy Nguyen",
        "team": "Golden State Warriors",
        "position": "Small Forward",
        "points": 20,
        "rebounds": 50,
        "assists": 1
    }
}
```

#### **Route: /players/\<int:id>/**

- Request Verb: DELETE
- Function: Deletes an existing player from the database
- Required Arguments: id
- Authentication: jwt_required
- Authorization: Admin only - get_jwt_identity
- Example Request: N/A
- Example Response:
```JSON
{
    "Message": "Player with id: 4 successfully deleted."
}
```
### Squad Routes

#### **Route: /squad/**

- Request Verb: GET
- Function: Returns all squad players of your own squad
- Required Arguments: N/A
- Authentication: jwt_required
- Authorization: N/A
- Example Request: N/A
- Example Response:
```JSON
[
{
    "message": "Here is your squad!",
    "squad": [
        {
            "id": 1,
            "user": {
                "name": "Johnny Bravo"
            },
            "players": {
                "name": "Stephen Curry"
            }
        }
    ]
}
]
```

#### **Route: /squad/\<int:user_id>/**

- Request Verb: GET
- Function: Returns all squad players of user_id
- Required Arguments: user_id
- Authentication: jwt_required
- Authorization: N/A
- Example Request: N/A
- Example Response:
```JSON
{
    "message": "Here is the squad for user_id:2!",
    "squad": [
        {
            "id": 1,
            "players": {
                "name": "Stephen Curry"
            }
        },
        {
            "id": 4,
            "players": {
                "name": "Lebron James"
            }
        }
    ]
}
```

#### **Route: /players/add/\<int:id>/**

- Request Verb: POST
- Function: Adds a player to the user's squad
- Required Arguments: id
- Authentication: jwt_required
- Authorization: N/A
- Example Request: N/A
- Example Response:
```JSON
{
    "Message": "Player successfully added to Squad",
    "Squad": {
        "players": {
            "name": "James Harden"
        }
    }
}
```

#### **Route: /squad/remove/\<int:id>/**

- Request Verb: DELETE
- Function: Deletes a player from squad
- Required Arguments: id
- Authentication: jwt_required
- Authorization: N/A
- Example Request: N/A
- Example Response:
```JSON
{
    "Message": "Player successfully removed from Squad"
}
```
