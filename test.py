import asyncio

from proxy_www import www, http, https, POST, GET


async def test():
    async def async_test():
        print('async call')
        resp = await www.github.com
        print(resp)

    async def async_secure_test():
        print('secure in async call')
        req: www = www.github.com.secure()
        print('Request :', req)
        print('Is secure? :', req.is_secure)
        print(await req)

    async def div_test():
        http_member_req = http.www.github.com
        print(http_member_req)
        print(await http_member_req)
        div_path_req = www.github.com/'profile'
        print(div_path_req)
        print(await div_path_req)

    def sync_test():
        print('sync call')
        resp = www.github.com()
        print(resp)

    async def https_test():
        resp = await https.github.com
        print(resp)

    async def method_with_params():
        # https://api.koreanbots.dev/v1
        resp = await (https.api.koreanbots.dev / 'v1/bots/get/541645954256863252')[GET](
            headers={"content-type": "application/json"}
        )
        print(await resp.json())

    await method_with_params()


asyncio.get_event_loop().run_until_complete(test())
