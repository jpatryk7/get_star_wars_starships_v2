import unittest
import requests
import random
import pymongo
from get_ships import *


class TestGetShips(unittest.TestCase):
    def setUp(self) -> None:
        self.starships_obj = GetShips()

        self.starships_json = requests.get("https://swapi.dev/api/starships/?page=1").json()
        self.random_starships_index = random.randint(0, len(self.starships_json["results"]) - 1)
        self.expected_ships_random_entry = self.starships_json["results"][self.random_starships_index]

        self.people_json = requests.get("https://swapi.dev/api/people/?page=1").json()
        self.not_allowed_keys = ["height", "age"]
        self.expected_all_pilots_format = {
            "1st entry": {
                "key": "_id",
                "datatype": str
            },
            "2nd entry": {
                "key": "name",
                "datatype": str
            },
            "3rd entry": {
                "not_allowed": self.not_allowed_keys
            }
        }
        self.connection_url = "mongodb://localhost:27017/"
        self.db_name = "starwars"
        self.collection_name = "characters"
        self.db = pymongo.MongoClient("mongodb://localhost:27017/")[self.db_name]
        self.db_collection = self.db[self.collection_name]

    def test_all_ships_length(self) -> None:
        expected = self.starships_json["count"]
        actual = len(self.starships_obj.all_ships)
        self.assertEqual(expected, actual)

    def test_all_ships_random_entry(self) -> None:
        expected = self.expected_ships_random_entry
        actual = self.starships_obj.all_ships[self.random_starships_index]
        self.assertEqual(expected, actual)

    def test_all_pilots_count_le(self) -> None:
        # le = less or equal
        expected = self.people_json["count"]
        actual = len(self.starships_obj.all_pilots)
        self.assertTrue(actual <= expected)

    def test_all_pilots_entry_length(self) -> None:
        expected = [3 for _ in self.starships_obj.all_pilots]
        actual = [len(p) for p in self.starships_obj.all_pilots.items()]
        self.assertEqual(expected, actual)

    def test_all_pilots_entry_format(self) -> None:
        expected = self.expected_all_pilots_format
        # test for each pilot
        for pilot in self.starships_obj.all_pilots.items():
            # test for each entry in pilot dictionary
            for key, expected_val in expected.items():
                if key == "3rd entry":
                    self.assertNotIn(expected_val[key], pilot.keys())
                else:
                    self.assertIn(expected_val[key], pilot.keys())
                    self.assertIsInstance(expected_val[key], pilot[expected_val[key]])

    def test__get_random_entry(self) -> None:
        doc = {"key1": 0, "key2": 0, "key3": 0, "key4": 0, "key5": 0, "key6": 0, "key7": 0}
        expected = doc.keys()
        actual = self.starships_obj._get_random_entry(doc)
        self.assertIn(expected, actual)

    def test__get_random_entry_provided_not_allowed(self) -> None:
        doc = {"key1": 0, "key2": 0, "key3": 0, "key4": 0, "key5": 0, "key6": 0, "key7": 0}
        not_allowed = ["key3", "key5"]
        expected = ["key1", "key2", "key4", "key6", "key7"]
        actual = self.starships_obj._get_random_entry(doc, not_allowed)
        for _ in range(20):
            self.assertIn(expected, actual)

    def test__get_pilot_id(self) -> None:
        pilot_info_entry = {
            "_id": "",
            "name": "Anakin Skywalker",
            "hair_color": "blond"
        }
        expected = str(self.db_collection.find(
            {
                "name": "Anakin Skywalker",
                "hair_color": "blond"
            },
            {
                "_id": True
            }).next())
        actual = self.starships_obj._get_pilot_id(pilot_info_entry, self.collection_name)
        self.assertEqual(expected, actual)

    def test__swap_url_with_id_provided_multiple_ships(self) -> None:
        starships = [
            {
                "name": "X-wing",
                "model": "T-65 X-wing",
                "manufacturer": "Incom Corporation",
                "cost_in_credits": "149999",
                "length": "12.5",
                "max_atmosphering_speed": "1050",
                "crew": "1",
                "passengers": "0",
                "cargo_capacity": "110",
                "consumables": "1 week",
                "hyperdrive_rating": "1.0",
                "MGLT": "100",
                "starship_class": "Starfighter",
                "pilots": [
                    "https://swapi.dev/api/people/1/",
                    "https://swapi.dev/api/people/9/",
                    "https://swapi.dev/api/people/18/",
                    "https://swapi.dev/api/people/19/"
                ],
                "films": [
                    "https://swapi.dev/api/films/1/",
                    "https://swapi.dev/api/films/2/",
                    "https://swapi.dev/api/films/3/"
                ],
                "created": "2014-12-12T11:19:05.340000Z",
                "edited": "2014-12-20T21:23:49.886000Z",
                "url": "https://swapi.dev/api/starships/12/"
		    }
        ]
        expected = [
            {
                "name": "X-wing",
                "model": "T-65 X-wing",
                "manufacturer": "Incom Corporation",
                "cost_in_credits": "149999",
                "length": "12.5",
                "max_atmosphering_speed": "1050",
                "crew": "1",
                "passengers": "0",
                "cargo_capacity": "110",
                "consumables": "1 week",
                "hyperdrive_rating": "1.0",
                "MGLT": "100",
                "starship_class": "Starfighter",
                "pilots": [
                    str(self.db_collection.find({"name": "Anakin Skywalker"}, {"_id": True}).next()),
                    str(self.db_collection.find({"name": "Biggs Darklighter"}, {"_id": True}).next()),
                    str(self.db_collection.find({"name": "Wedge Antilles"}, {"_id": True}).next()),
                    str(self.db_collection.find({"name": "Jek Tono Porkins"}, {"_id": True}).next())
                ],
                "films": [
                    "https://swapi.dev/api/films/1/",
                    "https://swapi.dev/api/films/2/",
                    "https://swapi.dev/api/films/3/"
                ],
                "created": "2014-12-12T11:19:05.340000Z",
                "edited": "2014-12-20T21:23:49.886000Z",
                "url": "https://swapi.dev/api/starships/12/"
		    }
        ]
        actual = self.starships_obj._swap_url_with_id(ships=starships)
        self.assertEqual(expected, actual)

    def test_save_starships_collection(self) -> None:
        is_saved = self.starships_obj.save_starships_collection(self.collection_name)
        self.assertTrue(is_saved)

        expected = self.collection_name
        actual = self.db.list_collection_names()
        self.assertIn(expected, actual)
