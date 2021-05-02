import asyncio
import aiohttp


class ClassPropertyMeta(type):
    def __getattribute__(self, attr):
        print(f'ClassPropertyMeta().{attr}')
        instance = self(url=f'http://www.{attr}')
        return instance

class www(metaclass=ClassPropertyMeta):
    url: str
    def __init__(self, url: str):
        self.url = url
        # print(f'www() -> url = {url}')
    
    def __getattribute__(self, attr):
        if attr in ('__dict__', 'url'):
            return super().__getattribute__(attr)
        # print(f'www.{attr}')
        # print(f'{self.url} -> {self.url}.{attr}')
        self.url += f'.{attr}'
        return self
    def __await__(self):
        session = aiohttp.ClientSession()
        resp = session.get(url=self.url).__await__()
        return resp
        
async def test():
    resp = await www.github.com
    print(resp)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(test())
