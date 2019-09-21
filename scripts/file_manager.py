import os

class FileManager:
	"""
	This class provides functions related to file management required for the indexer
	"""

	def __init__(self, root, accepted_formats):
		"""
		initialize variables: root path and accepted formats for the indexer
		"""
		self.root = root
		self.accepted_formats = accepted_formats


	def get_all_files(self):
		"""
		List all files recursively in the root specified by root
		"""
		files_list = []
		for path, subdirs, files in os.walk(self.root):
		    for name in files:
		    	files_list.append(os.path.join(self.root, name))
		return files_list


	def get_files_to_be_processed(self):
		"""
		returns list of files to be included in the index
		set `root` variable to the desired root
		:return: list of files to be processed
		"""
		files = self.get_all_files()
		files_list = []
		for name in files:
			if(name.split('.')[-1] in self.accepted_formats and os.stat(os.path.join(self.root, name)).st_size < 5000000):
				files_list.append(os.path.join(self.root, name))
		return files_list[0:-1]