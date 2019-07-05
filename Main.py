import asyncio, json, urllib.parse, http.cookies
http.cookies._is_legal_key = lambda _: True
import requests as _requests
from pypresence import Presence
from datetime import datetime
import time, threading
from manifest import Manifest

BASE_ROUTE = "https://www.bungie.net/Platform"
ACTIVITY_LOOKUP = BASE_ROUTE + "/Destiny2/{0}/Profile/{1}/Character/{2}/?components=CharacterActivities"

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

client_id = '596381603522150421'
RPC = Presence(client_id) 
RPC.connect()

with open("config.json", "r") as out:
    config = json.load(out)

requests = Requests(config["api_token"])
decoder = Decoder()

while True:
    activity_data = requests.get(ACTIVITY_LOOKUP.format("4", "4611686018468394612", "2305843009343475210"))
    activity_hash = activity_data["Response"]["activities"]["data"]["currentActivityHash"]
    activity_data_decoded = decoder.decode_hash(activity_hash, "DestinyActivityDefinition", "en")

    mode_hash = activity_data["Response"]["activities"]["data"]["currentActivityModeHash"]
    mode_data = decoder.decode_hash(mode_hash, "DestinyActivityModeDefinition", "en")

    with open("test.txt", "w+") as out:
        json.dump(activity_data_decoded, out, indent=4)
    with open("test2.txt", "w+") as out:
        json.dump(mode_data, out, indent=4)

    details, state = "In Orbit", ""
    print(mode_data)
    if activity_data_decoded["isPvp"]:
        state += "Crucible, "
    if mode_data != None:
        details = mode_data["displayProperties"]["name"]
    state += activity_data_decoded["displayProperties"].get("name", "In Orbit")

    party_size = [
        1,
        int(activity_data_decoded["matchmaking"]["maxParty"])
    ]

    RPC.update(
        state=state, details=details,
        large_image="willsmith", large_text="Placeholder", 
        small_image="destiny2_logo", small_text="Destiny 2",
        party_size=party_size, start=time.time()
    )
    time.sleep(15)