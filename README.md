# Working with The Star Wars API using GetShips class
API can accessed at https://swapi.dev/
## Setup
1. Ensure MongoDB Community Server, Database Tools and Shell are set up and added to path
2. Extract all characters from https://swapi.dev/api/people/ and save as a collection via MongoDB Compas or MongoDB Shell
3. Clone the repository and adjust database_name, people_collection_name, starship_collection_name, people_url_base, starships_url_base and connection_url if required
## Running
1. Open terminal in the directory with projects or create a new directory
2. Clone repository `$ git clone https://github.com/jpatryk7/get_star_wars_starships.git`
3. Cd into the project directory `$ cd get_star_wars_starships`
4. Create a new virtual environment `$ python -m venv my_venv`
5. Lunch venv (Windows) `$ source ./my_venv/Scripts/activate`, (Linux/MacOS) `$ source my_venv/bin/activate`
6. Install requirements `$ pip install -r requirements.txt`
7. (Optional) Adjust settings.py (general) `$ <file-editor-name> settings.py`, (Windows) `$ notepad settings.py`, (Linux/MacOS) `$ vi settings.py`
8. Run get_ships.py `$ python -m get_ships`