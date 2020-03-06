import json

config_file = 'config.json'
with open(config_file) as cf_file:
    config_dict = json.load(cf_file)
# Configuration parameters - IPs, Inputs, Stream IDs

	# Set elemental_ip 
elemental_ip = config_dict['elemental_ip']

# Mapper of GPI inputs to Elemental live streams
	# Example - We want GPI signal on pin 21 to trigger Ad Avail on Stream with ID = 5
	# 21: '5'
	# All must be seperated by commas
gpi2stream = config_dict['gpi_to_event']
