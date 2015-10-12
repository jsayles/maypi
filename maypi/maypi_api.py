import json
import base64
import logging
import requests

from random import randint
from Crypto.Cipher import AES
from django.conf import settings

class MaypAPIException(Exception):
	pass

def get_crypto(key=None):
	if not key:
		key = settings.MAYPI_API_KEY
	key = key[:32].zfill(32)
	return AES.new(key, AES.MODE_ECB)
	
def wrap_data(json_data, api_key=None):
	# Load to make sure we have valid json data
	json.loads(json_data)
		
	# Data must be a length that is a multiple of 16
	padding = 5120
	if len(json_data) < 1024:
		padding = 1024
	elif len(json_data) > padding:
		padding = len(json_data) * 16
	padded_data = json_data.ljust(padding)
	
	# Encrypt the data
	crypto = get_crypto(api_key)
	encrypted_data = crypto.encrypt(padded_data)
	
	# For tranport we also base64 encode the data
	encoded_data = base64.urlsafe_b64encode(encrypted_data)
	
	return encoded_data

def unwrap_data(encoded_data, api_key=None):
	# FDecode the base64 encodiing
	decoded_data = base64.urlsafe_b64decode(encoded_data.encode("utf-8"))
	
	# Decrypt the data
	crypto = get_crypto(api_key)
	decripted_data = crypto.decrypt(decoded_data)
	
	# Turn the data in to json
	json_data = json.loads(decripted_data)
	
	return json_data

def transmit_data(data):
	post_data = { 
		'door_id': settings.MAYPI_DOOR_ID,
		'data': wrap_data(data, api_key=settings.MAYPI_API_KEY),
	}
	return requests.post(settings.MAYPI_MASTER_URL, data=post_data)

def sync_door_codes():
	# TODO 
	# - Compile a give-me-all-your-door codes command in some form of json
	# - Use transmit_data to send it over to the mother ship
	# - Save all the door codes that come back to the local database
	sync_command = "{'action':'give-me-all-your-door-codes'}"
	response = transmit_data(sync_command)
	response_data = response.json()
	for door_code in response_data:
		# Save that shit to our database
		pass
		
	return
	
def random_code():
	return randint(100000, 999000)