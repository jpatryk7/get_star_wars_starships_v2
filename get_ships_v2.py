from typing import Any
import requests
import pymongo
import settings
import json
import uuid
import time
from bson.objectid import ObjectId


class GetShipsV2:
    def __init__(self, *,
                 connection_url: str = settings.connection_url,
                 starships_url_base: str = settings.starships_url_base,
                 people_url_base: str = settings.people_url_base,
                 starship_collection_name: str = settings.starship_collection_name,
                 people_collection_name: str = settings.people_collection_name,
                 database_name: str = settings.database_name) -> None:

        self.timer_record = {}

        # Setting up MongoDB connection
        self.db = pymongo.MongoClient(connection_url)[database_name]
        self.people_collection = self.db[people_collection_name]
        self.starship_collection = self.db[starship_collection_name]

        self.starships_url_base = starships_url_base
        self.people_url_base = people_url_base

    def __timer(self, position: str, pid: str, description: str = "") -> None:
        """
        Times blocks of code using "start" to save the current time and later, "stop" to find the difference between
        the current time and the previously saved one.

        :param position: "start" / "stop"
        :param pid: short name (alias) of the process
        :param description: description of the timed process
        :return:
        """
        if position not in ["start", "stop"]:
            raise Exception(f"Position can only take following arguments: {['start', 'stop']}. Got {position} instead")

        if position == "start":
            # on start create a dictionary with last_recorded_time, duration and description embedded within a field
            # with key = process_id in self.timer_record dictionary
            if pid in self.timer_record.keys():
                self.timer_record[pid]["last_recorded_time"] = time.time()
            else:
                self.timer_record[pid] = {
                    "last_recorded_time": time.time(),
                    "duration": 0.0,
                    "description": description
                }
        else:
            # on check update duration and last_recorder_time based on current time
            self.timer_record[pid]["duration"] += time.time() - self.timer_record[pid]["last_recorded_time"]
            self.timer_record[pid]["last_recorded_time"] = time.time()

    def __write_timer_log(self, dir_name: str = "timer_log/") -> None:
        """
        Save recorder timer values as json file
        :param dir_name: output directory
        :return:
        """
        path = dir_name + str(time.time()) + ".json"
        with open(path, 'w') as f:
            json.dump(self.timer_record, f, sort_keys=True, indent=4)

    def _get_pilot_name(self, pilot_url: str) -> str:
        """
        Access url and extract value of the "name" field.

        :param pilot_url: url to the pilot entry in API
        :return: name of the pilot
        """
        self.__timer("start", "get_requests_total")
        name = requests.get(pilot_url).json()["name"]
        self.__timer("stop", "get_requests_total")
        return name

    def _get_pilot_id(self, pilot_name: str) -> ObjectId:
        """
        Access the collection of characters and find an ID of a person with matching name.
        :param pilot_name: name of the pilot
        :return: pilot's ID
        """
        self.__timer("start", "pymongo_total")
        pilot_id = self.people_collection.find_one({"name": pilot_name})["_id"]
        self.__timer("stop", "pymongo_total")
        return pilot_id

    def _replace(self, elem1: Any, elem2: Any, arr: list) -> list:
        """
        Replace elem1 with elem2 in arr and return the new list.
        """
        for i, elem in enumerate(arr):
            if elem == elem1:
                arr[i] = elem2
        return arr

    def save_starships_collection(self) -> None:
        """
        Transform self.all_ships with _get_pilot_id() and _swap_url_with_id(). Then, write the list to the
        self.starship_collection.

        :return: list of all ships with
        """
        all_ships, page_index = [], 1
        # iterate through pages of starships to limit number of get requests
        while True:
            self.__timer("start", "get_requests_total")
            starships_json = requests.get(f"{self.starships_url_base}?page={page_index}").json()
            self.__timer("stop", "get_requests_total")
            # iterate through starships on the page
            for starship in starships_json["results"]:
                # iterate through pilots in the
                for pilot_url in starship["pilots"]:
                    pilot_name = self._get_pilot_name(pilot_url)  # url -> name
                    pilot_id = self._get_pilot_id(pilot_name)  # name -> id
                    # update starship variable
                    starship["pilots"] = self._replace(pilot_url, pilot_id, starship["pilots"])
                # save updated starship to the list
                all_ships.append(starship)

            # continue while loop until there is no url given in the "next" entry within page's content
            if starships_json["next"]:
                page_index += 1
            else:
                break

        # clear up collection before saving
        self.starship_collection.delete_many({})
        # save collection
        self.starship_collection.insert_many(all_ships)

        self.__write_timer_log()


if __name__ == "__main__":
    get_starships_obj = GetShipsV2()
    get_starships_obj.save_starships_collection()
