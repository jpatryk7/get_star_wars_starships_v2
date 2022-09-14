class GetShips:
    def __init__(self, url: str = "mongodb://localhost:27017/") -> None:
        pass

    def _get_all_ships(self, url_base: str = "https://swapi.dev/api/starships/") -> list[dict]:
        """
        Iterate through all pages (if using the default url_base: "https://swapi.dev/api/people/?page=page_index") to
        get parts of the ships' collection as a list. Merge lists at the end return.

        Function can take following forms:
            _get_all_ships()
            _get_all_ships("https://some.custom/url/to/api/entries/")

        :param url_base: url to starship list. Default: https://swapi.dev/api/starships/
        :return: list of all starships
        """
        return [{}]

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
        return ""

    def _get_all_pilots_info(self, url_base: str = "https://swapi.dev/api/people/") -> dict[dict]:
        """
        Iterate through all pages (if using the default url_base: "https://swapi.dev/api/people/?page=page_index") and
        save url as the key to each entry where entry is the name of the character and arbitrarily chosen key-value
        pair - the latter serves as an extra verification in case if there are two characters with the same name. Each
        entry of the dictionary e.g.:

        "https://swapi.dev/api/people/1/": {
            "_id": "",
            "name": "Luke Skywalker",
            "hair_color": "blond"
        }

        Function can take following forms:
            _get_all_ships()
            _get_all_ships("https://some.custom/url/to/api/entries/")

        :param url_base: url to characters list. Default: https://swapi.dev/api/people/
        :return: dictionary with characters urls as the key for each entry and dictionary as the value.
        """
        return dict(dict())

    def _get_pilot_id(self, pilot_info_entry: dict, collection_name: str = "characters") -> None:
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
        :return:
        """
        return None

    def _swap_url_with_id(self, ship_index: int = 0, *, ships: dict = None)\
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

    def save_starships_collection(self, collection: str = "starships") -> bool:
        """
        Create a new collection with ships and save the self.all_ships list in it.

        Function can take following forms:
            save_starships_collection()                         # collection name will be "starships"
            save_starships_collection("some_collection_name")   # collection name will be "some_collection_name"

        :param collection: name of the collection. Default: "starships"
        :return: true if the operation was successful and false otherwise
        """
        return True
