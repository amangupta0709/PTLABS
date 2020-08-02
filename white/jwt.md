# JWT Token

### Why JWT

* there are two types of web tokens:

  1. Session web tokens
2. JSON web tokens (JWT)
  
  The problen with session web tokens is that there is one session id which is sent by the client to the server and then the server use it to validate the details of the client using that session id.
  
BUT what if the database get lost then all the session will expire or if the web server is dynamic which create the same issue.
  
Then comes the JWT which includes user data as well as signature by the server so that server dont need to store session id in database. they can just look at user's signed data and validate it.

### Structure of JWT

* JWTs generally have three parts: a header, a payload, and a signature.

  * The header identifies which algorithm is used to generate the signature, and looks something like this:

    ```
    header = '{"alg":"HS256","typ":"JWT"}'
    ```

    `HS256` indicates that this token is signed using HMAC-SHA256.

  * The payload contains the claims that we wish to make:

    ```
    payload = '{"loggedInAs":"admin","iat":1422779638}'
    ```

    As suggested in the JWT spec, we include a timestamp called `iat`, short for "issued at".
    
  * The signature is calculated by base64url encoding the header and payload and concatenating them with a period as a separator:
  
    ```
    key = 'secretkey'
    unsignedToken = encodeBase64(header) + '.' + encodeBase64(payload)
    signature = HMAC-SHA256(key, unsignedToken)
    ```
  
    Multiple signature methods can be used to ensure the integrity of JWT:
  
    - RSA based
    - Elliptic curves
    - HMAC
    - None
  
  * To put it all together, we base64url encode the signature, and join together the three parts using periods:
  
    ```
    token = encodeBase64(header) + '.' + encodeBase64(payload) + '.' + encodeSHA256(signature)
    
    # token is now:
    eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsb2dnZWRJbkFzIjoiYWRtaW4iLCJpYXQiOjE0MjI3Nzk2Mzh9.gzSraSYS8EXBxLN_oWnFSRgCzcmJmMjLiuyu5CSpyHI
    ```

### Vulnerability

* The **None** Algorithm:

  When web servers just look at the `type of algorithm` and then decode the signature using that algorithm for validation, then this vulnerability occur.

  If the client sends the web token with algorithm type as **None** and edit the **payload** and set the signature as an **empty string** for example:

  `Header.payload.` (no string after second . )

* None algorithm was created by developers to verify empty strings during debugging. This was probably introduced to debug applications. 

* To prevent this web server should verify that the algorithm type in header shouldn't be **None** .