import json, urllib.parse, http.cookies
http.cookies._is_legal_key = lambda _: True
import requests as _requests
from pypresence import Presence
import time, datetime
from os import mkdir, path
from modules.manifest import Manifest

BASE_ROUTE = "https://www.bungie.net/Platform"
ACTIVITY_LOOKUP = BASE_ROUTE + "/Destiny2/{0}/Profile/{1}/Character/{2}/?components=CharacterActivities"
CHARACTER_LOOKUP = BASE_ROUTE + "/Destiny2/{0}/Profile/{1}/?components=Characters"
MEMBERSHIP_ID_LOOKUP = BASE_ROUTE + "/Destiny2/SearchDestinyPlayer/{0}/{1}"

class Config:
    def __init__(self):
        self.filepath = "./siva_files/config.json"

    def load(self):
        with open(self.filepath, "r") as out:
            config = json.load(out)
        return config

    def save(self, new_config):
        with open(self.filepath, "w+") as out:
            json.dump(new_config, out, indent=4)

    def get_conversion_table(self, table):
        _index = _requests.get("https://raw.githubusercontent.com/TheTimebike/SIVA/master/conversion_tables/index.json")
        _data_url = _index.json()[table]
        _data = _requests.get(_data_url)
        return _data.json()      

class Decoder:
    def __init__(self, headers):
        self._manifest = Manifest(headers)

    def decode_hash(self, hash, definition, language):
        return self._manifest._decode_hash(hash, definition, language)

class Requests:
    def __init__(self, api_token=None, interface=None):
        self.api_token = api_token
        self.interface = interface
        self.headers = {"X-API-Key": self.api_token}

    def get(self, request):
        _data = _requests.get(urllib.parse.quote(request, safe=':/?&=,.'), headers=self.headers)
        self._requestData = _data.json()
        if self._requestData.get("ErrorCode", False) == 2101:
            self.interface.error("1")
            return
        return self._requestData

def get_last_played_id(membershipType, membershipID, requests):
    url = CHARACTER_LOOKUP.format(membershipType, membershipID)
    character_data = requests.get(url)
    epoch_character_table = {}
    for key, attr in character_data["Response"]["characters"]["data"].items():
        epoch_character_table[convert_datestring_to_epoch(attr["dateLastPlayed"])] = key

    for epoch, id in epoch_character_table.items():
        if epoch == max(epoch_character_table.keys()):
            return id

def convert_datestring_to_epoch(datestring):
    unix_epoch = datetime.datetime(1970, 1, 1)
    log_dt = datetime.datetime.strptime(datestring.replace("T", " ").replace("Z", ""), "%Y-%m-%d %H:%M:%S")
    seconds_from_epoch = (log_dt - unix_epoch).total_seconds()
    return seconds_from_epoch

class Main:
    def __init__(self):
        self.run = True

    def start_siva(self, packaged_data, interface):
        client_id = '596381603522150421'
        RPC = Presence(client_id)
        RPC.connect()

        Config().save(packaged_data)
        config = Config().load()

        platform_enum_conversion_table = Config().get_conversion_table("platform")

        requests = Requests(config["api_token"], interface)
        decoder = Decoder(requests.headers)

        user_membership_type = platform_enum_conversion_table[config["platform"]]
        user_membership_data = requests.get(MEMBERSHIP_ID_LOOKUP.format(user_membership_type, config["username"]))["Response"]
        if len(user_membership_data) == 0:
            interface.error("2")
            return

        user_membership_id = user_membership_data[0]["membershipId"]

        while True:
            try:
                if not self.run:
                    RPC.close()
                    return

                last_played_character = get_last_played_id(user_membership_type, user_membership_id, requests)
                image_conversion_table = Config().get_conversion_table("image")
                state_conversion_table = Config().get_conversion_table("state")
                details_conversion_table = Config().get_conversion_table("details")

                activity_data = requests.get(
                    ACTIVITY_LOOKUP.format(
                        user_membership_type, 
                        user_membership_id, 
                        last_played_character
                        )
                    )
                activity_hash = activity_data["Response"]["activities"]["data"]["currentActivityHash"]
                activity_data_decoded = decoder.decode_hash(activity_hash, "DestinyActivityDefinition", "en")

                mode_hash = activity_data["Response"]["activities"]["data"]["currentActivityModeHash"]
                mode_data = decoder.decode_hash(mode_hash, "DestinyActivityModeDefinition", "en")

                # Default Arguments
                details, state = "In Orbit", "In Orbit"
                party_size = [1,1]
                picture, timer = "in_orbit", time.time()

                if mode_data != None:

                    details = mode_data["displayProperties"]["name"]
                    state = activity_data_decoded["displayProperties"].get("name", "In Orbit")
                    picture = activity_data_decoded["displayProperties"]["name"].lower().replace(" ", "_")
                    timer = convert_datestring_to_epoch(activity_data["Response"]["activities"]["data"]["dateActivityStarted"])
                    
                    remove_list = [",", "(", ")", ":"]
                    for char in remove_list:
                        picture = picture.replace(char, "")

                    if activity_data_decoded["isPvP"]:
                        details = "Crucible, " + mode_data["displayProperties"]["name"]
                        picture = "crucible"

                RPC.update(
                    state=state_conversion_table.get(state, state), 
                    details=details_conversion_table.get(details, details),
                    large_image=image_conversion_table.get(picture, picture),
                    small_image="destiny2_logo", small_text="Destiny 2",
                    start=timer
                )
                time.sleep(30)
            except Exception as ex:
                print(ex)
