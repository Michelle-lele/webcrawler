from configparser import ConfigParser
import os


package_directory = os.path.dirname(os.path.abspath(__file__))


def read_db_config(filename='config.ini', section='mysql'):
	""" Read database configuration file and return a dictionary object
		:param filename: name of the configuration file
		:param section: section of database configuration
		:return: a dictionary of database parameters
	"""
	parser = ConfigParser()

	if parser.read(os.path.join(package_directory, filename)):
		db_config = {}
		if parser.has_section(section):
			items = parser.items(section)
			for item in items:
				db_config[item[0]] = item[1]
			return db_config
		else:
			raise Exception(f'{section} not found in the {filename} file')
	else:
		raise Exception(f'{filename} file not found')


if __name__ == '__main__':
	config = read_db_config('config.ini', 'mysql')
	print(config)
