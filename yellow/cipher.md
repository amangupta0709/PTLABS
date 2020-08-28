# Cipher block chaining

follow the following steps:

- create a user with a username similar to the desired username.
- modify the first bytes of the cookie to become the username you are trying to become.

[CLICK HERE FOR PYTHON SCRIPT](cbc.py)

### Theory

CBC is an encryption mode in which the message is split into blocks of X bytes length and each block is encrypted separately using a key.

![License](https://pentesterlab.com/cbc/CBC_encryption.png)

We are going to focus on the first block as with our current  username, we only need one block. The schema below illustrates the  decryption process with an arbitrary IV:

![CBC decryption basics](https://pentesterlab.com/cbc/cbc-1.png)

If you create a user `bdmin`, this is what you get during the decryption:

![CBC decryption with bdmin](https://pentesterlab.com/cbc/cbc-2.png)

Now, we want to tamper with the IV (since it gets xored with the result of the decryption) to become `admin`:

![CBC decryption to become admin](https://pentesterlab.com/cbc/cbc-3.png)

### Exploit

Here, you will need to work out the block size. Based on the size of the cookie, it's very likely that the block size is 8 bytes. However, you  can play with the size of the username to detect this (like we did in  the **ECB exercise**.

Once you have the block size, it's likely that the first block is the IV.



we will make a user with username `bdmin`.



we can do some logical calculation.

The Cookie we got is base64 encoded after decoding we get this `IV + ouruser` so that means first byte of decoded cookie is first byte of IV.

the **first byte of IV** is `I` and **first byte of our user** is `b` 

we need to convert bdmin to admin

let first byte of **our intermediate cipher text** is `C` 

so, **`C XOR I` = b** 		=> 		**`b XOR I` = C**

as we can tamper with the IV =>	**`C XOR ?` = a** 

so, we get , 	**`a XOR C` = ?**

replacing C with above => 	**`a XOR (b XOR I)` = ?**

so now if we put replace first byte of IV with **?** we get first byte of user as **a** which will make bdmin to admin.