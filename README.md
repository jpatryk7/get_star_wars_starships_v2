# ETL Pipeline for starships on Star Wars API
API can be accessed at https://swapi.dev/. The code is meant to extract documents on starships from SWAPI; these docs 
have entries like name, films, crew, pilots, etc. The pilots field is an array with URLs to each pilot of the ship. We 
are interested in finding the IDs of these pilots in a local database and replacing URLs with them. Finally, the data is meant
to be saved as a collection locally.
## Setup
1. Ensure MongoDB Community Server, Database Tools and Shell are set up and added to the path
2. Extract all characters from https://swapi.dev/api/people/ and save them as a collection via MongoDB Compas or MongoDB Shell
3. Open the terminal in the directory with projects or create a new directory
4. Clone repository `$ git clone https://github.com/jpatryk7/get_star_wars_starships.git`
5. Cd into the project directory `$ cd get_star_wars_starships`
6. Create a new virtual environment `$ python -m venv my_venv`
7. Lunch venv (Windows) `$ source ./my_venv/Scripts/activate`, (Linux/macOS) `$ source my_venv/bin/activate`
8. Install requirements `$ pip install -r requirements.txt`
9. (Optional) Adjust settings.py (general) `$ <file-editor-name> settings.py`, (Windows) `$ notepad settings.py`, (Linux/macOS) `$ vi settings.py`
10. Run get_ships.py `$ python -m get_ships`

## Automatic Setup
> Follow steps 1 through 5 from the above section.
> 6. (Optional) Adjust settings.py (general) `$ <file-editor-name> settings.py`, (Windows) `$ notepad settings.py`, (Linux/macOS) `$ vi settings.py`
> 7. Run `$ source ./setup/local.sh`
>
> **Currently, tested only on Windows 10.**

## Code Breakdown
* MongoDB client is instantiated in `__init__()` function, where also `_get_all_ships()` and `_get_all_pilots_info()` ale used to extract data from on starships and people from the API.
* `_get_all_ships()` extracts data on starships from the API and saves it as a list of dictionaries.
* `_get_all_pilots_info()` extracts all pilots (i.e. people with a non-empty array in starships entry) from the API and saves their URL, name and a random entry (extra validation). It also creates an empty-values key-value pair for the _id field. The data are saved in a dictionary of dictionaries where each key of the outermost dict is the URL.
* `save_starship_collection()` loops through calls for `_swap_url_with_id()` for each starship in all_ships. Then, it saves the updated list of starships to a local collection.
* `_swap_url_with_id()` iterates through all pilots of a starship with a specified index and replaces each URL with a locally stored character ID. The ID is found using `_get_pilot_id()`.
* `_get_pilot_id()`  searches the local collection of characters and matches the name and the other (random). The ID is converted to bson.objectid.ObjectId and returned.
* `__timer()` and `_get_random_entry()` are "helper functions". The first one times blocks of code and displays messages in the console. The latter on the other hand takes in any dictionary and an optional list of excluded fields and returns a randomly chosen key.