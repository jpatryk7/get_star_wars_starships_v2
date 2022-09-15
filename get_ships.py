import requests
import random
import pymongo
import settings


class GetShips:
    def __init__(self, *,
                 connection_url: str = settings.connection_url,
                 starships_url_base: str = settings.starships_url_base,
                 people_url_base: str = settings.people_url_base,
                 starship_collection_name: str = settings.starship_collection_name,
                 people_collection_name: str = settings.people_collection_name,
                 database_name: str = settings.database_name) -> None:
        self.db = pymongo.MongoClient(connection_url)[database_name]
        self.people_collection = self.db[people_collection_name]
        self.starship_collection = self.db[starship_collection_name]

        self.starships_url_base = starships_url_base
        self.people_url_base = people_url_base

        self.all_ships = self._get_all_ships()
        self.all_pilots = self._get_all_pilots_info()

    def _get_all_ships(self) -> list[dict]:
        """
        Iterate through all pages (if using the default swapi.dev: "https://swapi.dev/api/people/?page=page_index") to
        get parts of the ships' collection as a list. Merge lists at the end return.

        :return: list of all starships
        """
        all_ships, page_index = [], 1
        while True:
            starships_json = requests.get(f"{self.starships_url_base}?page={page_index}").json()
            all_ships.extend([starship for starship in starships_json["results"]])
            if starships_json["next"]:
                page_index += 1
            else:
                break
        return all_ships

    def _get_random_entry(self, doc: dict, not_allowed: list = None) -> str:
        """
        Randomise a key name from the doc dictionary.

        Let:
            doc = {
                "name": "Some Name",
                "age": 20,
                "height": 182,
                "eye_color": "blue",
                "is_employed": False
            }

        Function can take following forms:
            _get_random_entry(doc)                              # function randomises through all keys in doc
            _get_random_entry(doc, ["is_employed", "height"])   # function randomises through "name", "age" and
                                                                  "eye_color"

        :param doc: dictionary
        :param not_allowed: list of entries that should be excluded from the random choice
        :return: randomly chosen key name from the doc
        """
        key_list = [key for key in [*doc] if key not in not_allowed]
        return random.choice(key_list)

    def _get_all_pilots_info(self) -> dict[dict]:
        """
        Iterate through all pages (if using the default url: "https://swapi.dev/api/people/?page=page_index") and
        save url as the key to each entry where entry is the name of the character and arbitrarily chosen key-value
        pair - the latter serves as an extra verification in case if there are two characters with the same name. Each
        entry of the dictionary should look like this e.g.:

        "https://swapi.dev/api/people/1/": {
            "_id": "",
            "name": "Luke Skywalker",
            "hair_color": "blond"
        }

        :return: dictionary with characters urls as the key for each entry and dictionary as the value.
        """
        all_pilots, page_index = {}, 1
        while True:
            people_json = requests.get(f"{self.people_url_base}?page={page_index}").json()
            for person in people_json["results"]:
                not_allowed = [
                    "_id", "name", "homeworld", "films", "species",
                    "vehicles", "starships", "created", "edited", "url"
                ]
                random_entry_key = self._get_random_entry(person, not_allowed)
                all_pilots[person["url"]] = {
                    "_id": "",
                    "name": person["name"],
                    random_entry_key: person[random_entry_key]
                }
            if people_json["next"]:
                page_index += 1
            else:
                break
        return all_pilots

    def _get_pilot_id(self, pilot_info_entry: dict) -> str:
        """
        Access the collection of characters and find an ID of a person with matching name and other key-value pair. Save
        its ID to the dictionary. ID of the character must be a string. E.g.: "ObjectId('6321a1f964d4eea3381c3be6')"

        Function can take following forms:
            _get_pilot_id(pilot_info_entry)
            _get_pilot_id(pilot_info_entry, "some_collection_name")     # uses "some_collection_name" instead of
                                                                          "characters" for accessing collection with
                                                                          star wars characters

        :param pilot_info_entry: single pilots name and an extra parameter. E.g.:
                {
                    "_id": "",
                    "name": "Anakin Skywalker",
                    "hair_color": "blond"
                }
        :return: pilot ID as a string
        """
        return ""

    def _swap_url_with_id(self, ship_index: int = 0, *, ships: list = None)\
            -> list:
        """
        Access ship with given index and if there is no pilots return empty list; if there is any use its URL as key for
        the all_pilots dictionary to get its ID. Then swap the URL with ID.

        Function can take following forms:
            _swap_url_with_id(9)                                # access ship with index number 9 in self.all_ships
            _swap_url_with_id(ships=some_user_defined_ship)     # use 0th item from some_user_defined_ship as the
                                                                  dictionary with data about a ship.
                                                                  some_user_defined_ship must be a dictionary within
                                                                  a list.

        :param ship_index: index of the ship in self.all_ships or ships if not None
        :param ships: list of ship(s) to use instead of the default self.all_ships
        :return: list of the same dimensions as self.all_ships[ship_index]["pilots"] but with id's instead of urls.
        """
        return []

    def lookup_starships_list(self, ship_index: int = -1, *, keys: list = None) -> None:
        """
        Allows to preview list of all starships.

        Function can take following forms:
            lookup_starships_list()                         # view all starships' info
            lookup_starships_list(6)                        # view all info about a starship with index 6
            lookup_starships_list(6, keys=["pilots"])       # view only pilots of the starship with index 6
            lookup_starships_list(keys=["name", "pilots"])  # view the name and pilots of all starships

        :param ship_index: index of the starship. If set/left to -1 shows all starships
        :param keys: list of keys from all ships or self.all_ships[ship_index] to view
        :return:
        """

    def save_starships_collection(self) -> None:
        """
        Transform self.all_ships with _get_pilot_id() and _swap_url_with_id(). Then, write the list to the
        self.starship_collection.

        :return:
        """
        for pilot_info in self.all_pilots:
            id = self._get_pilot_id(pilot_info)
        return None


if __name__ == "__main__":
    get_starships_obj = GetShips()
