# Unix Commands

### Find commands

* To find a file of name .bash_history in home directory

  ```bash
  find /home -name .bashrc
  ```

* To find a line containing PTLAB_KEY or any regex pattern in .bashrc file

  ```bash
  find /home -name .bashrc -exec grep PTLAB_KEY {} \;
  ```

  to find a line starting with word 'passwd' 

  ```bash
  grep '^passwd' .bash_history
  ```

* find 1 line after a line containing word 'passwd'  in .bash_history file 

  ```bash
  grep -A 1 passwd .bash_history
  ```

  note: -A for after -B for before



### Extraction commands

* to decompress gzip then extract and verbose a backup.tgz file which is a tar gzip file.

  ```bash
  tar -zxvf backup.tgz
  ```

  -z for gzip in .tgz

  -j for bzip2 in .tbz

* to compress file in cpio format

  ```bash
  cpio -ov > file
  ```

  to decompress

  ```bash
  cpio -iv < file
  ```

  to make directories and doesn't make absolute filenames

  i.e, if a file is extracted in /home/victim/secrets.txt instead of this we make our own directories using -d and provide --no-absolute-filenames to remove '/' from starting path

  so it will make home/victim/secrets.txt in current folder not in /home folder

  ```bash
  cpio -idv --no-absolute-filenames < file
  ```

* openssl encryption in aes256 format

  ```bash
  openssl enc -aes256 -k yourkey -in ./myfile -out ./abcd.enc
  ```

  for decryption add -d

  ```bash
  openssl enc -aes256 -d yourkey -in ./abcd.enc -out ./myfile
  ```

### Mysql commands

* basics

  ```mysql
  show DATABASES;
  use [DATABASE]
  show TABLES;
  SELECT * FROM [TABLE]
  ```

* for accessing a file

  ```mysql
  select load_file('/var/lib/mysql-files/key.txt')
  ```

### Postgresql commands

* for authentication

  ```shell
  psql -d databasename -U user
  ```

  then type the password for that user

* basics

  ```sql
  \list
  \c [database]
  \dt
  SELECT * FROM [table];
  ```

* for accessing a file

  ```sql
  CREATE TABLE black(a text);
  COPY black from '/var/lib/postgresql/9.4/key.txt';
  SELECT * FROM black;
  
  DROP TABLE black;
  ```

### SQLite3 commands

* access the database file of name database.db

  ```shell
  sqlite3 database.db
  ```

* basics

  ```sqlite
  .tables
  SELECT * FROM tablename;
  ```

* 

