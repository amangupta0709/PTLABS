# JWT

[Click Here for Python Script](jwt_rs_to_hs.py)

### Vulnerability

Multiple signature methods can be used to ensure the integrity of JWT:

- RSA based
- Elliptic curves
- HMAC
- None

With RSA, to:

- sign a token, you need the private key.
- verify a token, you can use the public key corresponding to the private key used for the signature.

With HMAC, to:

* sign a token, you need the secret.
* verify a token, you need the same secret.

In practice, you can change the algorithm used by the application (RSA - `RS256`) to tell it to use HMAC (`HS256`). The application will call the method verify when you send the cookie. Since the code is written to use RSA, it will call `verify(public_key, data)`. But since the algorithm is set to HMAC, it will end up calling `HMAC(public_key,data)`. 

The application will verify the signature with the public key but  since you are forcing the application to use HMAC, it will actually  verify the signature with `HMAC(public_key, data)`. As an attacker, you have everything you need to generate a valid signature, since the public key is actually public. 