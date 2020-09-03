# JWT Key Id Sql Injection

[Click Here for python script](jwt_kid.py)

This issue comes from one of the fields in the header: `kid`. This parameter is available in some libraries, it's short for `key identifier`. In this application, the `kid` is used without proper escaping to retrieve the key. This lack of escaping could lead to multiple types of vulnerabilities:

- SQL injections.
- Directory traversals.
- ...

### Theory

we see that in kid value it is taking key from a variable key1 `"kid":"key1"`

if we do `"key1' union select 'abcd"` then if will select key as key1 which will return actual key value as well as select abcd which will return 'abcd' string

but just after taking value as key1 it will verify the signature it won't check for value abcd.

So, we will do `"kid":"blahblah' union select 'abcd"` . Now, random string `blahblah` won't return anything so it will go check for `abcd` .

So, now it will verify with key `abcd` so now we will sign that too with key `abcd`

