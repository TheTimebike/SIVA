import asyncio, json, urllib.parse, http.cookies
http.cookies._is_legal_key = lambda _: True
import requests as _requests
from pypresence import Presence
from datetime import datetime
import time, threading
from manifest import Manifest

BASE_ROUTE = "https://www.bungie.net/Platform"
ACTIVITY_LOOKUP = BASE_ROUTE + "/Destiny2/{0}/Profile/{1}/Character/{2}/?components=CharacterActivities"
CHARACTER_LOOKUP = BASE_ROUTE + "/Destiny2/{0}/Profile/{1}/?components=Characters"

class Decoder:
    def __init__(self):
        self._manifest = Manifest(requests.headers)

    def decode_hash(self, hash, definition, language):
        return self._manifest._decode_hash(hash, definition, language)

class Requests:
    def __init__(self, api_token=None):
        self.api_token = api_token
        self.headers = {"X-API-Key": self.api_token}

    def get(self, request):
        print(request)
        _data = _requests.get(urllib.parse.quote(request, safe=':/?&=,.'), headers=self.headers)
        self._requestData = _data.json()
        return self._requestData

def get_last_played_id(membershipType, membershipID):
    url = CHARACTER_LOOKUP.format(membershipType, membershipID)
    character_data = requests.get(url)
    epoch_character_table = {}
    for key, attr in character_data["Response"]["characters"]["data"].items():
        epoch_character_table[convert_datestring_to_epoch(attr["dateLastPlayed"])] = key
    
    for epoch, id in epoch_character_table.items():
        if epoch == max(epoch_character_table.keys()):
            return id

def convert_datestring_to_epoch(datestring):
    datetime_string = datestring.replace("Z", "").replace("T", " ")
    target_timestamp = time.strptime(datetime_string, '%Y-%m-%d %H:%M:%S')
    mktime_epoch = time.mktime(target_timestamp)
    return mktime_epoch + 3382
    

client_id = '596381603522150421'
RPC = Presence(client_id) 
RPC.connect()

with open("config.json", "r") as out:
    config = json.load(out)

requests = Requests(config["api_token"])
decoder = Decoder()

while True:
    activity_data = requests.get(ACTIVITY_LOOKUP.format("4", "4611686018468394612", get_last_played_id("4", "4611686018468394612")))
    activity_hash = activity_data["Response"]["activities"]["data"]["currentActivityHash"]
    activity_data_decoded = decoder.decode_hash(activity_hash, "DestinyActivityDefinition", "en")

    mode_hash = activity_data["Response"]["activities"]["data"]["currentActivityModeHash"]
    mode_data = decoder.decode_hash(mode_hash, "DestinyActivityModeDefinition", "en")

    timer = convert_datestring_to_epoch(activity_data["Response"]["activities"]["data"]["dateActivityStarted"])

    with open("test.txt", "w+") as out:
        json.dump(activity_data_decoded, out, indent=4)
    with open("test2.txt", "w+") as out:
        json.dump(mode_data, out, indent=4)

    # Default Arguments
    details, state = "In Orbit", "In Orbit"
    party_size = [1,1]
    picture = "in_orbit"

    if mode_data != None:
        details = mode_data["displayProperties"]["name"]
        state = activity_data_decoded["displayProperties"].get("name", "In Orbit")
        picture = activity_data_decoded["displayProperties"]["name"].lower().replace(" ", "_")
        remove_list = [",", "(", ")"]
        for char in remove_list:
            picture = picture.replace(char, "")
    
        print(picture)
        print(details)
        print(state)

        if activity_data_decoded["isPvP"]:
            details = "Crucible, " + mode_data["displayProperties"]["name"]
            picture = "crucible"

    swap_conversion_table = {
        "the_menagerie:_the_menagerie_heroic": "the_menagerie",
        "zero_hour_heroic": "zero_hour",
        "landing_zone": "mercury",
        "leviathan:_normal": "leviathan",
        "leviathan:_prestige": "leviathan",
        "the_reckoning:_tier_i": "the_reckoning",
        "the_reckoning:_tier_ii": "the_reckoning",
        "the_reckoning:_tier_iii": "the_reckoning",
        "last_wish:_level_55": "last_wish",
        "crown_of_sorrow:_normal": "crown_of_sorrows"
    }

    user_conversion_table = {
        "Last Wish: Level 55": "Last Wish",
        "The Menagerie: The Menagerie (Heroic)": "The Menagerie: (Heroic)",
        "Landing Zone": "Mercury"

    }
    print(swap_conversion_table.get(picture, picture))
    print(user_conversion_table.get(state, state))
    RPC.update(
        state=user_conversion_table.get(state, state), details=details,
        large_image=swap_conversion_table.get(picture, picture),
        small_image="destiny2_logo", small_text="Destiny 2",
        start=timer
    )
    time.sleep(30)