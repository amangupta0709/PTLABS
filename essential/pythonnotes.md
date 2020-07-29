# Classes and Method Resolution Order(MRO)

* let say a variable `a='abc'` , to see which class it belongs to

  ```python
  a = 'abc'.__class__
  ```

  OUTPUT: `<class 'str'>`

  to see the base class of this class:

  ```python
  a = ''.__class__.mro()
  ```

  `mro()` it is a method which lists the list of classes in the base class of the present class.

  `__mro__` for tuple not list

  OUTPUT: `[<class 'str'>, <class 'object'>]`

  ```python
  a = True.__class__.mro()
  ```

  OUTPUT: `[<class 'bool'>, <class 'int'>, <class 'object'>]`

* to make this variable 'a' an `object` instead of `string`

  ```python
  a = ''.__class__.mro()[1]
  ```

  OUTPUT: `<class 'object'>`

* Now to list the `subclasses` of class `object` we use

  `__subclasses__()`

  ```python
  a = ''.__class__.mro()[1].__subclasses__()
  ```

  OUTPUT: long list of subclasses

* IN PYTHON 2  'object' is at index=2 and subproccess.Popen is at 233

  so for python2

  ```python
  a = ''.__class__.mro()[2].__subclasses__()[233]
  ```



**Reference** : https://www.lanmaster53.com/2016/03/11/exploring-ssti-flask-jinja2-part-2/