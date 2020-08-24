# API to Shell

the exploitation of two vulnerabilities: 

- A weakness in a signature check due to PHP type confusion.
- A call to PHP `unserialize`.

Using the first bug, you will be able to retrieve the source code of  the application. Then, using this code, you will be able to find a call  to `unserialize` and exploit it. 



The application allows you to download and upload files. A signature  protects the download functionality. Only the server can issue a correct signature. You can retrieve a valid signature for your files by using  the `list` API call.

To get started, register an account, upload a file, list all your files and retrieve the file you just uploaded. 

When you are retrieving a file, you can tamper with the signature `sig` and see that any modification to this value will prevent you from accessing this file.

### Signature Check

When the application receives a request to access a protected resource, it will compute the signature based on the `secret` and the part of the HTTP request (the `uuid` parameter in this exercise). Then the application will compare the  signature computed with the one provided by the client. If they match,  the client will get the resource. If they don't match and error will be  returned. 

### PHP Comparisions

* PHP provides two ways to compare two variables: 

  - Loose comparison using `==`/`!=`. Both variables have "the same value”.
  - Strict comparison using `===`/`!==`. Both variables have "the same type and the same value”.

* Comparision example in php interactive shell:

  ```php
  % php -a
  Interactive shell
  
  php > var_dump("1" === 1);
  bool(false)
  php > var_dump("1" == 1);
  bool(true)
  ```

* Surprising behaviour

  ```php
  php > var_dump("a" == 0);
  bool(true)
  php > var_dump("1' or 1=1" == 1);
  bool(true)
  php > var_dump("<script>alert(1)</script>" == 0);
  bool(true)
  ```

### Impact of using JSON

* One of the key thing with JSON is that the person calling the API can decide on the type of data.
* Using the fact that we can force the type of the signature, we can  decide what the type of the signature is, we can force a comparison  between a string and an integer and hope that the application is using a loose comparison.
* The following example illustrate how the computed hash will match a signature using a loose comparison:
  - If the computed hash starts with `0` (followed by a letter) or starts by a letter: `a` to `f`; it will be equal to `0`.
  - If the computed hash starts with `19ee` it will be equals to `19`.
  - If the computed hash starts with `3fee` it will be equals to `3`.
* You can solve this problem using two methods:
  - You can tamper with the `uuid` parameter and compare it to the signature `0`.
  - You can tamper with the `uuid` and play with the signature `sig` by increasing the value of `sig` (starting from `0`).

##### Efficient Way

* Using the most efficient method (first method), you can play with the `uuid` value and set the signature to `0`:

  - `"uuid": "../../../etc/passwd"; "sig": 0;`
  - `"uuid": "../../.././etc/passwd"; "sig": 0;`
  - `"uuid": "../../../././etc/passwd"; "sig": 0;`
  - `"uuid": "../../.././././etc/passwd"; "sig": 0;`

  Until you find a value for which you can use a signature of `0` and get the file. Adding `./` will still give you the same file but the application will generate a different signature that may be loosely equal to `0`. 

### Unserialize Exploitation

In PHP, if the application unserializes data under your control, you  can potentially trigger unexpected behavior. To do so, you will need to  find an object with a call to one of these "trampoline" functions:

- `__wakeup()` when an object is unserialized.
- `__destruct()` when an object is deleted.
- `__toString()` when an object is converted to a string.

By reviewing the source code of the application, you probably discovered that the `token` used for authentication was a serialized `User` object signed using a HMAC. However, the `User` class does not use any of the function listed above. To exploit this issue, we will need to use another class. The class `File` seems to contain everything we need: 

```php
<?php

class File {
  public $owner,$uuid, $content;
  public $logfile = "/var/www/logs/application.log";

  function __destruct() {
    // Loogging access 
    $fd = fopen($this->logfile, 'a');
    fwrite($fd, $_GET['action'].":".$this->uuid.' by '.$this->owner."\n");
    fclose($fd);
  }
[...]
```

First, we need to piece together all we need to generate a token:

- a serialized `File` object with our malicious payload.
- a valid signature for this object using the code and the `KEY` available in the application's source code. 

Now, that we can generate a token, we are going to exploit this issue in two steps:

- Use the call do `__destruct()` to create a PHP file in the web root of the application.
- Access this PHP file.

The final trick for this exercise is to find the right API action to call, you need to remember that the application expects a `User` object and you are providing a `File` object. If the application calls a method of the `User` class on the `File` class, it will crash.



**SEE PAYLOAD HERE: [payload](payload)**



## Vim Usage for Formatting

```
vim /\\n/\r/g
```

for replacing \n with \r

```
/\//g
```

for replacing \ with nothing

