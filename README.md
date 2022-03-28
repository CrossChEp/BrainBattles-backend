# BrainBattles.api 
Valpha 1.0


    This api was made for BrainBattles backend

### How to use it?
The api allows you to make requests to endpoints that'll 
give you respond that contains data json

#### Endpoints:
Api contains some endpoints:

- Users' endpoints
- Game endpoints
- Queue endpoints
- Tasks endpoints
- Auth endpoint

#### Usage
### User's endpoints:
1. 

   
    GET /api/users
Endpoint that gets all users from database.
Example response:

2. 


    POST /api/register
endpoint that adds user to database

3. 


    DELETE /api/users
endpoint that deletes user from database


4. 


    PUT /api/users 
endpoint that updates user's data


### Tasks endpoints:

1. 

    
    POST /api/task
endpoint that adds task to database

2. 


    GET /api/tasks
endpoint that gets all tasks from database

3. 


    GET /api/task
endpoint that gets concrete task using task id

4. 


    DELETE /api/task
endpoint that deletes task from using task id

5. 


    GET /api/user_tasks
endpoint that gets user's tasks

### Queue endpoints:
1. 

    
    POST /api/matchmaking
endpoint that adds user to queue

2. 

    
    DELETE /api/matchmaking
endpoint that deletes user from queue


### Game endpoints:
1. 


    POST /api/game
endpoint for adding user to game


2. 


    DELETE /api/game/cancel
endpoint for deleting user from game

3. 


    POST /api/game/try
endpoint for making try


### Authorization endpoints

1. 


    /token
Gets jwt token


2. 


    /user/me
endpoint for getting current user
