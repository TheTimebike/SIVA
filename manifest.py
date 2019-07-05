import zipfile, os, sys, aiohttp, json, requests
from manifest_reader import ManifestReader

class Manifest:
	def __init__(self, headers=None):
		self.headers = headers
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
			'zh-cht': ''
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
		print(manifestJson)
		manifestUrl = 'https://www.bungie.net' + manifestJson['Response']['mobileWorldContentPaths'][language]
		manifestFileName = manifestUrl.split('/')[-1]
		
		if not os.path.isfile(manifestFileName):
			downloadedFileName = self._download_manifest(manifestUrl)
			if os.path.isfile("./{0}".format("manifest")):
				zip = zipfile.ZipFile("./{0}".format("manifest"), "r")
				zip.extractall("./")
				zip.close()
				os.remove("manifest")
				
		self.manifests[language] = manifestFileName
		
	def _download_manifest(self, request):
		_data = requests.get(request, headers=self.headers)
		#print(_data.content)
		downloadTarget = os.path.basename("manifest")
		with open(downloadTarget, "wb") as out:
			#while True:
			#	dataChunk = _data.content.read(1024)
			#	if not dataChunk:
			#		break
			out.write(_data.content)
		return "manifest"

	def _bumpAlong(self, val):
		val = int(val)
		if (val & (1 << (32 - 1))) != 0:
			val = val - (1 << 32)
		return val