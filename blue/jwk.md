# JWT JWK / CVE-2018-0114

[Click Here for python script](jwk.py)

The issue is very interesting. JWT allows users to embed public keys (using the `jwk` value) inside the header of the token. However, the application should  never trust those keys as an attacker can provide his own key and sign  the message using the corresponding private key.

We need `jwk` key in `header` part:

```
{
  "alg":"RS256",
  "jwk":  {
          "kty":"RSA",
          "kid":"bilbo.baggins@hobbiton.example",
          "use":"sig",
          "n":"n4EPtAOCc9Alke...........rNP5zw",
          "e":"AQAB"
          }
}
```

This is the format we will need to follow to get the right header for our payload to work.

In this `jwk` part we have to provide `n` and `e`  values it means that when verifying the key signature it will use these particular values to verify the signature

### Building our exploit

- Build the header with the right values for `n` and `e`.
- Sign the token using RSA with the private key that matches the `n` and `e` in the header.

