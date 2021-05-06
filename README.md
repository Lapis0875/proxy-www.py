# proxy-www.py
Python port of proxy-www (https://github.com/justjavac/proxy-www).
Implemented additional functionalities!

## How to install
```shell
pip install proxy-www
```

## Example
```py
from proxy_www import www, http, https, GET

async def some_func():
    resp = await www.github.com     # Basic proxy_www request
    http_resp = await http.github.com   # insecure proxy_www request using http
    https_resp = await https.github.com # secure proxy_www request using http
    
    secure_resp = await www.github.com.secure() # secure request with www.secure()
    insecure_resp = await www.github.com.insecure() # insecure request with www.insecure()
    req = www.github.com
    print(req.is_secure)    # boolean property indicating proxy_www request object is whether secure(https) or not (http).

    path_resp = await www.github.com / 'Lapis0875'  # ClassProxy objects (www, http, https) can append paths on url using '/' operator.

    
    # New in 1.1.0 : HTTP methods with [], request parameters with ()
    # Syntax : (www,http,https)[HTTPMethod or str](*args, **kwargs)
    # Example :
    get_req = await (https.api.koreanbots.dev / 'v1/bots/get/541645954256863252')[GET](
        headers={"content-type": "application/json"}
    )
    print(await resp.json())
```
