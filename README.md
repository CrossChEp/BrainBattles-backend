# BrainBattles.api 
VBeta 1.0


    This api was made for BrainBattles backend

The api allows you to make requests to get some data 
for BrainBattles app

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



