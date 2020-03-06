import requests as req
import dicttoxml
import time



class Elemental_api():
	def __init__(self, elemetnal_ip):
		self.elemental_ip = elemetnal_ip
		self.headers = {'Accept': 'application/xml', 'Content-type': 'application/xml'}
		self.cue_part_url = ''
		self.gen_cue_part_url()

	def list_live_events(self):
		endpoint = 'api/live_events'
		
		url_ip = 'http://{}/'.format(self.elemental_ip)
		url_events = '{}{}/'.format(url_ip,endpoint)
		# print(url_events)
		
		response = req.get(url_events, self.headers)
		return response.text

	def gen_cue_part_url(self):
		endpoint = 'api/live_events'		
		url_ip = 'http://{}/'.format(self.elemental_ip)
		url_events = '{}{}/'.format(url_ip,endpoint)

		self.cue_part_url = url_events


	def gen_stop_cue_body(self, stream_id):
				
		# Used only to copy/paste into the body variable in stop_cue
		body = {
			'cue_point':{
			'event_id': stream_id,
			'return_offset': 0
						}
				}
		bodyxml = dicttoxml.dicttoxml(body, root=False, attr_type=False)

		print(bodyxml)

	def start_cue(self, stream_id):
		# body string is taken from gen_cue_part_url function
		url = '{}{}/cue_point/'.format(self.cue_part_url, stream_id)
		body = '<cue_point><event_id>{}</event_id><splice_offset>0</splice_offset><duration>0</duration></cue_point>'.format(stream_id)
		
		response = req.post(url, headers = self.headers, data = body)
		return response

	def stop_cue(self, stream_id):
		# body string is taken from gen_stop_cue_body function
		url = '{}{}/cue_point/'.format(self.cue_part_url, stream_id)
		body = '<cue_point><event_id>{}</event_id><return_offset>0</return_offset></cue_point>'.format(stream_id)

		response = req.post(url, headers = self.headers, data = body)
		return response




	
