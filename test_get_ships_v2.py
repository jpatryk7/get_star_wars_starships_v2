import unittest

import settings
from get_ships_v2 import *


class TestGetShipsV2(unittest.TestCase):
    def setUp(self) -> None:
        self.ships_v2 = GetShipsV2()

        self.db = pymongo.MongoClient(settings.connection_url)[settings.database_name]
        self.characters_collection = self.db[settings.people_collection_name]

    def test__get_pilot_name(self) -> None:
        """
        Test if _get_pilot_name returns Luke Skywalker for url https://swapi.dev/api/people/1/
        :return:
        """
        expected = "Luke Skywalker"
        actual = self.ships_v2._get_pilot_name("https://swapi.dev/api/people/1/")
        self.assertEqual(expected, actual)

    def test__get_pilot_id(self) -> None:
        """
        Test if the returned ID corresponds to Luke Skywalker when given name Luke Skywalker
        :return:
        """
        expected_name = "Luke Skywalker"
        actual_id = self.ships_v2._get_pilot_id("Luke Skywalker")
        actual_name = self.characters_collection.find_one({"_id": actual_id})["name"]
        self.assertEqual(expected_name, actual_name)

    def test__replace(self) -> None:
        """
        Test if _replace swaps elements in a list
        :return:
        """
        input_list = [1, "ab", 604, 4, {"empty": "dict"}, "gsav"]
        expected = "sp34g"
        actual = self.ships_v2._replace({"empty": "dict"}, expected, input_list)
        self.assertIn(expected, actual)


if __name__ == "__main__":
    unittest.main()
