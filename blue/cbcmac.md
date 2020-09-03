# CBC Message Authentication Code

When IV is NULL BYTE : [Click here for ruby script](cbcmac.rb)

When IV is HARDCODED and delivered in cookie as well : [Click here for python script](cbcmac.py)

CBC-MAC is a method to ensure integrity of a message by encrypting it  using CBC mode and keeping the last encrypted block as "signature". This ensures that a malicious user can not modify any part of the data  without having to change the signature. The key used for the  "encryption" ensures that the signature can't be guessed.

we will use the fact that there is no protection in place to get the  application to sign two messages and build another message by  concatenating the two messages.

### Theory

let say we have a message of block size 8 :  `m` 

also we have another message of block size 8 : `m'`

we know that for single single block the `IV(Initialisation Vector)` is null IV or anything.

![img](https://pentesterlab.com/cbc-mac/cbc-mac-1.png)

**we can see that signatures generated for two independent messages `m` and `m'` are `t` and `t'` respectively**

but if we concatenate the two messages `m+m'` then we have 2 blocks of size 8 each

![img](https://pentesterlab.com/cbc-mac/cbc-mac-2.png)

we see that for more than one block **the IV of next block is the signature of previous block**



That means if we provide username as `t XOR m'` and it will get XOR with `IV` will produce `???` because XOR with NULL IV produce `t XOR m'` itself.

so that means : `(t XOR m') XOR NULL-IV` = `t XOR m'`

### Implementation

Now we need to get access to **administrator**

we will split it into 2 blocks of size 8 each as : 

- `administ`
- `rator\00\00\00`

After base64 decoding the cookie we get the cookie in format : 

`username--signature`

we will make user of username as `administ` and get signature as `t` 

**Now we will take XOR of `t` and `rator\00\00\00` and we will get `x`**

**now will login with username : `x` and signature as : `?`** 

**Now we will supply session cookie as `administrator--?`**







