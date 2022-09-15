import unittest

import settings
from get_ships import *


class TestGetShips(unittest.TestCase):
    def setUp(self) -> None:
        self.starships_obj = GetShips()

        self.starships_json = requests.get(f"{settings.starships_url_base}?page=1").json()
        self.random_starships_index = random.randint(0, len(self.starships_json["results"]) - 1)
        self.expected_ships_random_entry = self.starships_json["results"][self.random_starships_index]

        self.people_json = requests.get(f"{settings.people_url_base}?page=1").json()
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
        self.connection_url = settings.connection_url
        self.db_name = settings.database_name
        self.collection_name = settings.people_collection_name
        self.db = pymongo.MongoClient(self.connection_url)[self.db_name]
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
        actual = [len(p) for p in self.starships_obj.all_pilots.values()]
        self.assertEqual(expected, actual)

    def test_all_pilots_entry_format(self) -> None:
        expected = self.expected_all_pilots_format
        # test for each pilot
        for pilot in self.starships_obj.all_pilots.values():
            # test for each entry (except the random one) in pilot dictionary
            for key, expected_val in expected.items():
                if key != "3rd entry":
                    self.assertIn(expected_val["key"], pilot.keys())
                    self.assertIsInstance(pilot[expected_val["key"]], expected_val["datatype"])

    def test__get_random_entry(self) -> None:
        doc = {"key1": 0, "key2": 0, "key3": 0, "key4": 0, "key5": 0, "key6": 0, "key7": 0}
        expected = doc.keys()
        actual = self.starships_obj._get_random_entry(doc)
        self.assertIn(actual, expected)

    def test__get_random_entry_provided_not_allowed(self) -> None:
        doc = {"key1": 0, "key2": 0, "key3": 0, "key4": 0, "key5": 0, "key6": 0, "key7": 0}
        not_allowed = ["key3", "key5"]
        expected = ["key1", "key2", "key4", "key6", "key7"]
        actual = self.starships_obj._get_random_entry(doc, not_allowed)
        for _ in range(20):
            self.assertIn(actual, expected)

    def test__get_pilot_id(self) -> None:
        pilot_info_entry = {
            "_id": "",
            "name": "Anakin Skywalker",
            "hair_color": "blond"
        }
        expected = ObjectId(self.db_collection.find(
            {
                "name": "Anakin Skywalker",
                "hair_color": "blond"
            },
            {
                "_id": True
            }
        ).next()["_id"])
        actual = self.starships_obj._get_pilot_id(pilot_info_entry)
        self.assertEqual(expected, actual)

    def test__swap_url_with_id(self) -> None:
        self.starships_obj.all_ships = [
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
        self.starships_obj.all_pilots = {
            "https://swapi.dev/api/people/1/": {
                "_id": "",
                "name": "Anakin Skywalker",
                "hair_color": str(self.db_collection.find({"name": "Anakin Skywalker"}).next()["hair_color"])
            },
            "https://swapi.dev/api/people/9/": {
                "_id": "",
                "name": "Biggs Darklighter",
                "hair_color": str(self.db_collection.find({"name": "Biggs Darklighter"}).next()["hair_color"])
            },
            "https://swapi.dev/api/people/18/": {
                "_id": "",
                "name": "Wedge Antilles",
                "hair_color": str(self.db_collection.find({"name": "Wedge Antilles"}).next()["hair_color"])
            },
            "https://swapi.dev/api/people/19/": {
                "_id": "",
                "name": "Jek Tono Porkins",
                "hair_color": str(self.db_collection.find({"name": "Jek Tono Porkins"}).next()["hair_color"])
            }
        }
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
                    ObjectId(self.db_collection.find({'name': 'Anakin Skywalker'}).next()['_id']),
                    ObjectId(self.db_collection.find({'name': 'Biggs Darklighter'}).next()['_id']),
                    ObjectId(self.db_collection.find({'name': 'Wedge Antilles'}).next()['_id']),
                    ObjectId(self.db_collection.find({'name': 'Jek Tono Porkins'}).next()['_id'])
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

        self.starships_obj._swap_url_with_id(ship_index=0)
        actual = self.starships_obj.all_ships

        self.assertEqual(expected, actual)

    def test_save_starships_collection_coll_name(self) -> None:
        expected = settings.starship_collection_name
        actual = self.db.list_collection_names()
        self.assertIn(expected, actual)


if __name__ == "__main__":
    unittest.main()
