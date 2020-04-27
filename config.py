import json
# from helpers import setup_logger

WATCHED_FILES = ['config.json']
LAST_EXIT_FILE = 'last_exit.pkl'
STATE_FILE = 'gpi_pair_state.pkl'

config_file = 'config.json'

# das_logger = setup_logger()
try:
	with open(config_file) as cf_file:
		config_dict = json.load(cf_file)
except FileExistsError or FileNotFoundError:
	# das_logger.error('Nema config.json file, losho.')
	print('Nema config deistvaite!')

elemental_ip = config_dict['elemental_ip']
gpi2stream = config_dict['gpi_to_event']
min_av_enbl = config_dict['min_avail_enabled']
min_av_dur = config_dict['min_avail_duration']