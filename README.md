# Second Version of ETL Pipeline for Starships on Star Wars API
The code is meant to extract and edit documents from starships from [SWAPI](https://swapi.dev/) followed by uploading it to local MongoDB collection. It is a second iteration of the code trying to improve on efficiency. Refer to [previous version](https://github.com/jpatryk7/get_star_wars_starships) for more details.
## Setup
1. Ensure MongoDB Community Server, Database Tools and Shell are set up and added to the path
2. Extract all characters from https://swapi.dev/api/people/ and save them as a collection via MongoDB Compas or MongoDB Shell
3. Open the terminal in the directory with projects or create a new directory
4. Clone repository `$ git clone https://github.com/jpatryk7/get_star_wars_starships_v2.git`
5. Cd into the project directory `$ cd get_star_wars_starships_v2`
6. Create a new virtual environment `$ python -m venv my_venv`
7. Lunch venv (Windows) `$ source ./my_venv/Scripts/activate`, (Linux/macOS) `$ source my_venv/bin/activate`
8. Install requirements `$ pip install -r requirements.txt`
9. (Optional) Adjust settings.py (general) `$ <file-editor-name> settings.py`, (Windows) `$ notepad settings.py`, (Linux/macOS) `$ vi settings.py`
10. Run get_ships.py `$ python -m get_ships_v2`

## Automatic Setup
> Follow steps 1 through 5 from the above section. Then, adjust settings.py `$ <file-editor-name> settings.py` and run `$ source ./setup/local.sh`.
>
> **Currently, tested only on Windows 10.**

## Code Breakdown
* MongoDB client is instantiated in `__init__()` function
* `_get_pilot_name()` extracts pilot's name from dictionary at given url
* `_get_pilot_id()` finds pilot's id in local collection using their name
* `_replace()` replaces one element in a list with another; here, used to swap url with id in `"pilots"` entry in the starship dictionary
* `__timer()` is executed throughout the code to record and save duration of different blocks of code
* `__write_timer_log()` writes the dictionary with all timers' records into a `.json` file