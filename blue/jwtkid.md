# JWT Key ID

[Click here for Python Script](jwt_kid.py)

This issue comes from one of the fields in the header: `kid`. This parameter is available in some libraries, it's short for `key identifier`. In this application, the `kid` is used without proper escaping to retrieve the key. This lack of escaping could lead to multiple types of vulnerabilities:

- SQL injections.
- Directory traversals.
- ...

### Theory

the application uses `HS256` so that means it verifies and sign with the same.

so it takes key from `kid` parameter from header part and then verifies that the signature is signed with same key or not.

so now we will make signature signed by the key `""` it is empty key and then we will provide same in kid parameter `kid:../../../../../../dev/null` 

because `/dev/null` returns null value and we signed the signature with same empty key so it will bypass the verfication.



