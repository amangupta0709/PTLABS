# Play Session Injection

**Play Framework** is a web framework that allows developers to quickly build web  application in Java or Scala. The way the code is organised and the URL  are mapped are very similar to Ruby-on-Rails.

### Fingerprinting

Here the Play application is deployed on the port 80 and running as  root (to be able to bind on the port 80). We can observe that Play is  used by looking at the `Server` header:

```bash
$ echo -ne "HEAD / HTTP/1.1\r\nHost: vulnerable\r\nConnection: close\r\n\r\n" | netcat vulnerable 80 
HTTP/1.1 200 OK
Server: Play! Framework;1.2.5;prod
Content-Type: text/html; charset=utf-8
Set-Cookie: PLAY_FLASH=;Expires=Sun, 15-Jun-14 21:47:26 GMT;Path=/
Set-Cookie: PLAY_ERRORS=;Expires=Sun, 15-Jun-14 21:47:26 GMT;Path=/
Set-Cookie: PLAY_SESSION=;Expires=Sun, 15-Jun-14 21:47:26 GMT;Path=/
Cache-Control: no-cache
Content-Length: 2179
```

**SUGGESTION** : Running Play or any web server that doesn't drop privileges during its startup is obviously a terrible idea.

Since we can register an account, we will try to create a 'test:test1' account to look into the session's handling.

After registering this account, we receive the following cookie:

```
PLAY_SESSION=dc76c24ea96cdf0009188367583f07bee1126aff-%00___AT%3A103939fbeba60071e96c5dd505a7916d8b49c9c9%00%00user%3Atest%00
```

​      

We can see that information is stored in clear text in the session:  `user%3atest` (`user:test`). Unfortunately, no sensitive information is  stored as part of the session.   

### Play Session

The session mechanism used by Play is really similar to Rack sessions  (used by Ruby-on-Rails by default). The content of the session is sent  back to the clients instead of being stored server side. To prevent an  attacker from tampering his session.

### Theory

First, the code retrieve the cookie used for the session, for example `PLAY_SESSION`. If the cookie is present it will then split it into 2 parts:

- `sign`: the signature.
- `data`: the data.

It will then verify the signature using the method `Crypto.sign` and the secret key `Play.secretKey`. 

**NOTE: The `Play.secretKey` is stored in `conf/application.conf`, if you can  get access to this file (for example using a directory traversal), you  will be able to forge sessions.   **

the value inside the data is as following format:

`%00KEY1:VALUE1%00%00KEY2:VALUE2%00%00KEY3:VALUE3%00`

which can be re-aranged as below:

| %00  | **key1** | :    | **value1** | %00  |
| ---- | -------- | ---- | ---------- | ---- |
| %00  | **key2** | :    | **value2** | %00  |
| %00  | key3     | :    | value3     | %00  |

### Exploitation

The current session looks like:

| %00  | **___AT** | :    | **103939fbeba60071e96c5dd505a7916d8b49c9c9** | %00  |
| ---- | --------- | ---- | -------------------------------------------- | ---- |
| %00  | **user**  | :    | **our_username**                             | %00  |

As we can't edit the data so we inject code in username during registering a new user.

if we inject `abcd%00%00user:admin` in place of username, then session will look like:

| %00     | **___AT** | :     | 103939fbeba60071e96c5dd505a7916d8b49c9c9 | %00     |
| ------- | --------- | ----- | ---------------------------------------- | ------- |
| %00     | user      | :     | **abcd**                                 | **%00** |
| **%00** | **user**  | **:** | **admin1**                               | %00     |

So, we see user is over written.