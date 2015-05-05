import json
import base64
import logging
import requests

from Crypto.Cipher import AES
from django.conf import settings

crypto = AES.new(settings.MAYPI_API_KEY, AES.MODE_ECB)

class MaypAPIException(Exception):
	pass

def wrap_data(json_data):
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
	encrypted_data = crypto.encrypt(padded_data)
	
	# For tranport we also base64 encode the data
	encoded_data = base64.urlsafe_b64encode(encrypted_data)
	
	return encoded_data

def unwrap_data(encoded_data):
	# FDecode the base64 encodiing
	decoded_data = base64.urlsafe_b64decode(encoded_data.encode("utf-8"))
	
	# Decrypt the data
	decripted_data = crypto.decrypt(decoded_data)
	
	# Turn the data in to json
	json_data = json.loads(decripted_data)
	
	return json_data

def transmit_data(data):
	return requests.post(settings.MAYPI_MASTER_URL, data={'data':wrap_data(data)})
	