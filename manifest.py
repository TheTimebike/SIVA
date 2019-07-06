import zipfile, os, sys, aiohttp, json, requests
from manifest_reader import ManifestReader

class Manifest:
	def __init__(self, headers=None):
		self.headers = headers
		self.manifests = {
			'en': ''
		}
		
	def _decode_hash(self, hash, definition, language):
		if self.manifests.get(language.lower(), None) == None:
			print("Language Not Found")
		elif self.manifests.get(language.lower(), None) == "":
			self._update_manifest(language)
			
		if definition == "DestinyHistoricalStatsDefinition":
			hash = "\""+hash+"\""
			identifier = key
		hash = self._bumpAlong(hash)
		identifier = "id"
		
		with ManifestReader(self.manifests.get(language)) as _handler:
			_result = _handler.query(hash, definition, identifier)
			
		if len(_result) > 0:
			return json.loads(_result[0][0])
		return None
			
	def _update_manifest(self, language):
		if self.manifests.get(language.lower(), None) == None:
			print("Language Not Found")
		
		manifestJson = requests.get("https://www.bungie.net/Platform"+"/Destiny2/Manifest/", headers=self.headers).json()
		manifestUrl = 'https://www.bungie.net' + manifestJson['Response']['mobileWorldContentPaths'][language]
		manifestFileName = "./siva_files/" + manifestUrl.split('/')[-1]
		
		if not os.path.isfile(manifestFileName):
			downloadedFileName = self._download_manifest(manifestUrl)
			if os.path.isfile("./{0}".format("siva_files/manifest")):
				zip = zipfile.ZipFile("./{0}".format("siva_files/manifest"), "r")
				zip.extractall("./siva_files/")
				zip.close()
				
		self.manifests[language] = manifestFileName
		
	def _download_manifest(self, request):
		_data = requests.get(request, headers=self.headers)
		downloadTarget = "./siva_files/manifest"
		with open(downloadTarget, "wb") as out:
			out.write(_data.content)
		return downloadTarget

	def _bumpAlong(self, val):
		val = int(val)
		if (val & (1 << (32 - 1))) != 0:
			val = val - (1 << 32)
		return val