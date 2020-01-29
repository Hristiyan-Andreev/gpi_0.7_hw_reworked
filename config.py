# Configuration parameters - IPs, Inputs, Stream IDs

	# Set elemental_ip 
elemental_ip = '192.168.2.3'

# Mapper of GPI inputs to Elemental live streams
	# Example - We want GPI signal on pin 21 to trigger Ad Avail on Stream with ID = 5
	# 21: '5'
	# All must be seperated by commas
gpi2stream = {
		21: '5',
		13: '7',
}

# Time to wait after edge detection [sec]
wait_time = 5

# Locking interval for filtering short impulses [sec]
lock_interval = 0


# Dont touch
import os
class FlaskConfig(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'TEMALIVE'