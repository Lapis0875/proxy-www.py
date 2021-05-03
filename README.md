# proxy-www.py
Python port of proxy-www (https://github.com/justjavac/proxy-www).
Just purpose of practicing python metaclass and magic method overriding.
I don't think this is practical... but it's fun :rofl:

## How to install
```shell
pip install proxy-www
```

## Example
```py
from proxy_www import www, http, https

async def some_func():
    resp = await www.github.com     # Basic proxy_www request
    http_resp = await http.github.com   # insecure proxy_www request using http
    https_resp = await https.github.com # secure proxy_www request using http
    
    secure_resp = await www.github.com.secure() # secure request with www.secure()
    insecure_resp = await www.github.com.insecure() # insecure request with www.insecure()
    req = www.github.com
    print(req.is_secure)    # boolean property indicating proxy_www request object is whether secure(https) or not (http).

    path_resp = await www.github.com / 'Lapis0875'  # ClassProxy objects (www, http, https) can append paths on url using '/' operator.
```
