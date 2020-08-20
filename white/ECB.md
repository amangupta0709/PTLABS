# Electronic Code Book

ECB is an encryption mode in which the message is split into blocks  of X bytes length and each block is encrypted separately using a key.

The following schema explains this method:

![License](https://assets.pentesterlab.com/ecb/ECB_encryption.png)

During the decryption, the reverse operation is used. Using ECB has multiple security implications:

- Blocks from encrypted message can be removed without disturbing the decryption process.
- Blocks from encrypted message can be moved around without disturbing the decryption process.

### How to Detect

* If you create an account and log in two times with this account, you can see that the cookie sent by the application didn't change.

  **NOTE : ** If you log in many times and always get the same cookie, there is  probably something wrong in the application. The cookie sent back should be unique each time you log in. If the cookie is always the same, it  will probably always be valid and there won't be anyway to invalidate  it.    

* If we look at the cookie, we can see that it seems uri-encoded and base64-encoded:

  The 2 equals sign encoded as `%3d%3d` are a good indicator of base64-encoded string. after decoding it is hex string

  * username: kali1		password: abcd

    ```bash
    $ echo "SpaAuSzM+E9MT/qGLUc+OQ==" | base64 -d | hexdump -C
    0000000 964a b980 cc2c 4ff8 4f4c 86fa 472d 393e
    0000010
    ```

  * username: kali2         password: abcd

    ```bash
    $ echo "xGqYoQbHt2pMT/qGLUc+OQ==" | base64 -d | hexdump -C
    0000000 6ac4 a198 c706 6ab7 4f4c 86fa 472d 393e
    0000010
    ```

  we can see that the **2nd half part is same** `4c 4f fa 86 2d 47 3e 39` 

### Exploit Theory

* if we take username: 20 a's        password: 20 a's

  ```bash
  $ echo "9KG7Vr4LWlr0obtWvgtaWo2D+8a0/1du9KG7Vr4LWlr0obtWvgtaWp9nueYCQLuA" | base64 -d | hexdump
  0000000 a1f4 56bb 0bbe 5a5a a1f4 56bb 0bbe 5a5a
  0000010 838d c6fb ffb4 6e57 a1f4 56bb 0bbe 5a5a
  0000020 a1f4 56bb 0bbe 5a5a 679f e6b9 4002 80bb
  0000030
  ```

  we see `a1f4 56bb 0bbe 5a5a` is repeated pattern which is of 8 bits.

  a1 f4 56 bb 0b be 5a 5a    a1 f4 56 bb 0b be 5a 5a
  `83 8d c6 fb ff b4 6e 57`    a1 f4 56 bb 0b be 5a 5a
  a1 f4 56 bb 0b be 5a 5a    `67 9f e6 b9 40 02 80 bb` 

  these are extra characters.

* We can think of the encrypted stream has one of the two following possibilities: 

  - The stream contains the username, a delimiter and the password:

  ![Schema username password](https://assets.pentesterlab.com/ecb/del_u_p.png)

  - The stream contains the password, a delimiter and the username:

  ![Schema password username](https://assets.pentesterlab.com/ecb/del_p_u.png)

  By creating another user with a long username and a short password, we can see that the following pattern is used: `username|delimiter|password|delimiter`

* let's make a user with username: 16 a's     password 3 b's

  ```bash
  $ echo "9KG7Vr4LWlr0obtWvgtaWlrABKq5v9Cz" | base64 -d | hexdump -C
  00000000  f4 a1 bb 56 be 0b 5a 5a  f4 a1 bb 56 be 0b 5a 5a  
  00000010  5a c0 04 aa b9 bf d0 b3                           
  00000018
  ```

  we see that  `f4 a1 bb 56 be 0b 5a 5a` pattern is repeated twice which is of 8 bits,

  **hence we can confirm that the app is encrypting in block of 8 characters and making it as 8 bits encoding** 

  breakdown is as follows : `8 a's`  : `8 a's`  :  `delimiter+ 3b's` 

  as it only verifies the username for authentication

  means it will decrypt the first 2 break down of 8 a's and 8 a's and combine them and join them to check its username.

  so if we provide username as username: aaaaaaaaadmin   password:anything

  breakdown will be as follows : 

  `8 a's`  :  `admin + del` :`imiter + pa`: `ssword12`

  the second part  `admin+delimiter+password12`  is broken into 3 blocks of 8 bits for encryption.

  now we know already that first block is of `8 a's` so we can remove it and re-encode the string to get make the app believe that **my username is admin so it will allow as it ckecks only the username**.

