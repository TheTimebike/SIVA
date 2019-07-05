import sqlite3

class ManifestReader:
	def __init__(self, manifestFile):
		self.connection = sqlite3.connect(manifestFile)
		self.cursor = self.connection.cursor()
		
	def query(self, hash, definiton, identifier):
		sql = """
			  SELECT json from {0}
			  WHERE {1} = {2}
			  """.format(definiton, identifier, hash)
		self.cursor.execute(sql)
		return self.cursor.fetchall()
	
	def __enter__(self):
		return self

	def __exit__(self, *args):
		self.cursor.close()
		self.connection.close()
