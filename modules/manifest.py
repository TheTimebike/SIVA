import zipfile, os, sys, aiohttp, json, requests
from modules.manifest_reader import ManifestReader

class Manifest:
	def __init__(self, directory, headers=None):
		self.headers = headers
		self.directory = directory
		self.manifests = {
			'en': '',
			'fr': '', 
			'es': '', 
			'de': '', 
			'it': '', 
			'ja': '', 
			'pt-br': '', 
			'es-mx': '',
			'ru': '', 
			'pl': '', 
			'ko': '',
			'zh-cht': '',
			'zh-chs': ''
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
		
		manifestJson = requests.get("https://www.bungie.net/Platform/Destiny2/Manifest/", headers=self.headers).json()
		print(manifestJson)
		manifestUrl = 'https://www.bungie.net' + manifestJson['Response']['mobileWorldContentPaths'][language]
		manifestFileName = "./{0}/".format(self.directory) + manifestUrl.split('/')[-1]
		
		if not os.path.isfile(manifestFileName):
			downloadedFileName = self._download_manifest(manifestUrl)
			if os.path.isfile("./{0}/manifest".format(self.directory)):
				zip = zipfile.ZipFile("./{0}/manifest".format(self.directory), "r")
				zip.extractall("./{0}/".format(self.directory))
				zip.close()
				
		self.manifests[language] = manifestFileName
		
	def _download_manifest(self, request):
		_data = requests.get(request, headers=self.headers)
		downloadTarget = "./{0}/manifest".format(self.directory)
		with open(downloadTarget, "wb") as out:
			out.write(_data.content)
		return downloadTarget

	def _bumpAlong(self, val):
		val = int(val)
		if (val & (1 << (32 - 1))) != 0:
			val = val - (1 << 32)
		return val
