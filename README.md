# ETL Pipeline for starships on Star Wars API
API can be accessed at https://swapi.dev/
## Setup
1. Ensure MongoDB Community Server, Database Tools and Shell are set up and added to path
2. Extract all characters from https://swapi.dev/api/people/ and save as a collection via MongoDB Compas or MongoDB Shell
3. Open terminal in the directory with projects or create a new directory
4. Clone repository `$ git clone https://github.com/jpatryk7/get_star_wars_starships.git`
5. Cd into the project directory `$ cd get_star_wars_starships`
6. Create a new virtual environment `$ python -m venv my_venv`
7. Lunch venv (Windows) `$ source ./my_venv/Scripts/activate`, (Linux/MacOS) `$ source my_venv/bin/activate`
8. Install requirements `$ pip install -r requirements.txt`
9. (Optional) Adjust settings.py (general) `$ <file-editor-name> settings.py`, (Windows) `$ notepad settings.py`, (Linux/MacOS) `$ vi settings.py`
10. Run get_ships.py `$ python -m get_ships`
## Code Breakdown
to be continued