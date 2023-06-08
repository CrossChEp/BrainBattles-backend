# BrainBattles.api 
VBeta 1.0


    This api was made for BrainBattles backend

The api allows you to make requests to get some data 
for BrainBattles app

### BrainBattles matchmacking server(indev): https://github.com/CrossChEp/brainbattles-matchmaking-server
### BrainBattles game server(indev): https://github.com/CrossChEp/brainbattles-game-server/settings

# Project description
## The goal of the project
The goal of the project is to develop a system for competition between students.
Users can choose the subject, enter the game filtered
by their rank and subject. With the correct answer to the task, user gets
points, with which he gets himself a new rank. The higher the rank, the more privileges.
For example, users with an average rank get the opportunity to add, update and delete
THEIR tasks according to the rank.

Moreover, students will be able to unite in groups (clans) and fight with students from other clans,
filling their clan with rank and reputation.

This project is aimed at learning without fuss and cramming

# Quickstart
### 1.Clone the repo  "BrainBattles backend"
### 2. Create a new virtual environment 
#### ```python3 -m venv env```
### 3. Install all modules
#### ```pip install -r requirements.txt```
### 4. Update database
#### ```alembic upgrade head```
### 5. Download the redis:
* Linux(Ubuntu):
    #### `sudo apt install redis`
* Windows:

    Download the redis from official repository: https://github.com/MicrosoftArchive/redis/releases
### 6. Run redis:

* Linux(Ubuntu):
    #### ```redis-server start```
* Windows:
    #### `start redis-cli.exe`

### 7. Run the api
#### ```uvicorn run api:app```
## Now everything is working!

