from __future__ import annotations

import asyncio
import logging
from functools import partial
from sys import stdout

import aiohttp


logger = logging.getLogger('proxy_www')
handler = logging.StreamHandler(stdout)
handler.setFormatter(
    logging.Formatter(
        style='{',
        fmt='[{asctime}] [{levelname}] {name}: {message}'
    )
)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


class ClassProxyMeta(type):
    def __new__(cls, clsname: str, bases: tuple, attrs: dict):
        logger.debug('Creating new ClassProxy class with parameters : name={}, bases={}, attrs={}'.format(clsname, bases, attrs))

        def __init__(self, url: str):
            self.url: str = url

        __init__.__name__ = '{}.__init__'.format(clsname)

        def __getattr__(self, item):
            if item.startswith('__'):
                return super(ClassProxyMeta, self).__getattr__(item)
            logger.debug('{} : getattr > item = {}'.format(self.url, item))
            self.url += '.{}'.format(item)
            return self

        __getattr__.__name__ = '{}.__getattr__'.format(clsname)

        def __truediv__(self, other):
            if isinstance(other, str):
                self.url += '/{}'.format(other)
                print(self.url)
                return self
            else:
                return super().__floordiv__(other)

        __truediv__.__name__ = '{}.__truediv__'.format(clsname)

        def __await__(self) -> aiohttp.ClientResponse:
            session = aiohttp.ClientSession()
            resp = yield from session._request('GET', self.url).__await__()
            yield from session.close().__await__()
            logger.debug('{} -> GET : session closed? > {}'.format(self.url, session.closed))
            return resp

        __await__.__name__ = '{}.__await__'.format(clsname)

        def __repr__(self) -> str:
            return 'ClassProxy(class={}, url={})'.format(self.__class__.__name__, self.url)

        __repr__.__name__ = '{}.__repr__'.format(clsname)

        attrs.update({
            '__await__': __await__,
            '__truediv__': __truediv__,
            '__getattr__': __getattr__,
            '__init__': __init__,
            '__repr__': __repr__
        })

        logger.debug('Updated attrs for ClassProxy {}:'.format(clsname))
        logger.debug(attrs)
        logger.debug(super().__new__)
        return super(ClassProxyMeta, cls).__new__(cls, clsname, bases, attrs)

    def __getattr__(self, item):
        if item == '_asyncio_future_blocking':
            return super().__getattr__(item)
        logger.debug('Creating www proxy object for domain {}'.format(item))
        instance = self(url='http://www.{}'.format(item))
        return instance

    def __repr__(self) -> str:
        return 'ClassProxy(class={})'.format(self.__name__)


class www(metaclass=ClassProxyMeta):
    url: str

    @property
    def is_secure(self) -> bool:
        return self.url.startswith('https://')

    def secure(self):
        if not self.is_secure:
            self.url = self.url.replace('http', 'https')
        return self

    def insecure(self):
        if self.is_secure:
            self.url = self.url.replace('https', 'http')
        return self

    def __call__(self):
        # return self.__sync_req__()
        raise NotImplementedError('Currently, sync request using ClassProxy.__call__ is WIP. Sorry for inconvenience :(')

    def __sync_req__(self):
        task_name: str = 'www.Future({} -> GET)'.format(self.url)
        task: asyncio.Task = asyncio.create_task(self.__await__(), name=task_name)
        task.add_done_callback(partial(print, task_name))
        # result = next(future.__await__())
        # print(type(result), result)
        logger.debug('{}'.format(task_name, task))
        while True:
            if task.done():
                try:
                    return task.result()
                except asyncio.CancelledError:
                    return '{} has been cancelled :('.format(task_name, self.url)
                except Exception:
                    raise task.exception()


class http(metaclass=ClassProxyMeta):
    @property
    def is_secure(self) -> bool:
        return False


class https(metaclass=ClassProxyMeta):
    @property
    def is_secure(self) -> bool:
        return True


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

    def div_test():
        http_member_req = http.www.github.com
        print(http_member_req)
        div_path_req = www.github.com/'profile'
        print(div_path_req)

    def sync_test():
        print('sync call')
        resp = www.github.com()
        print(resp)

    async def https_test():
        resp = await https.github.com
        print(resp)

    sync_test()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(test())