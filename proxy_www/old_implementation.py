from __future__ import annotations

import aiohttp
import asyncio
import enum
import sys
import typing
from functools import partial

from proxy_www.utils import get_logger, wrap_class_method

logger = get_logger('proxy_www')


"""
DEPRECATED OLD CODES.
PRESERVED TO CHECK PREVIOUS IMPLEMENTATION LATER.
"""


class HTTPMethod(enum.Enum):
    GET = enum.auto()
    HEAD = enum.auto()
    POST = enum.auto()
    PUT = enum.auto()
    DELETE = enum.auto()
    CONNECT = enum.auto()
    OPTIONS = enum.auto()
    TRACE = enum.auto()
    PATCH = enum.auto()


for http_mtd in HTTPMethod:
    setattr(sys.modules[__name__], http_mtd.name, http_mtd)


class ClassProxyMeta(type):
    def __new__(mcs, clsname: str, bases: tuple, attrs: dict):
        logger.debug('Creating new ClassProxy class with parameters : name={}, bases={}, attrs={}'.format(clsname, bases, attrs))

        # Preserve original __init__ function.
        if '__init__' in attrs:
            logger.debug(f'Found pre-defined __init__ method in class {clsname}')
            original_init = attrs['__init__']

            @wrap_class_method(clsname)
            def __init__(self, url: str):
                self.url = url
                self.args = []
                self.kwargs = {}
                # call original __init__
                original_init(self, url)
        else:
            @wrap_class_method(clsname)
            def __init__(self, url: str):
                self.url = url
                self.args = []
                self.kwargs = {}

        @wrap_class_method(clsname)
        def __getattr__(self, item):
            if item in self.__dict__:
                print(f'{item} is in self.__dict__!')
                return self.__dict__[item]
            if item.startswith('__'):
                print(super(ClassProxyMeta, self).__getattr__)
                return super(ClassProxyMeta, self).__getattr__(item)
            logger.debug('{} : getattr > item = {}'.format(self.url, item))
            self.url += '.{}'.format(item)
            return self

        @wrap_class_method(clsname)
        def __truediv__(self, other):
            if isinstance(other, str):
                self.url += '/{}'.format(other)
                print(self.url)
                return self
            else:
                return super().__truediv__(other)

        @wrap_class_method(clsname)
        def __call__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs
            return self

        @wrap_class_method(clsname)
        def __await__(self) -> aiohttp.ClientResponse:
            session = aiohttp.ClientSession()
            resp = yield from session._request(self.method, self.url, *self.args, **self.kwargs).__await__()
            yield from session.close().__await__()
            logger.debug('{} -> {} : session closed? > {}'.format(self.url, self.method, session.closed))
            return resp

        @wrap_class_method(clsname)
        def __repr__(self) -> str:
            return 'ClassProxy(class={}, url={}, method={})'.format(self.__class__.__name__, self.url, self.method)

        @wrap_class_method(clsname)
        def __getitem__(self, method: typing.Union[str, HTTPMethod]):
            if type(method) is str:
                method = method.upper()
                if method not in HTTPMethod.__members__:
                    raise ValueError('HTTP Method must be one of valid HTTP methods, not {}'.format(method))
                self.method = method
            elif type(method) is HTTPMethod:
                self.method = method.name
            else:
                raise TypeError('HTTP Method must be HTTPMethod or string, not {}'.format(type(method)))

            return self

        attrs.update({
            '__await__': __await__,
            '__truediv__': __truediv__,
            '__getattr__': __getattr__,
            '__init__': __init__,
            '__repr__': __repr__,
            '__getitem__': __getitem__,
            'method': 'GET'
        })

        logger.debug('Updated attrs for ClassProxy {}:'.format(clsname))
        logger.debug(attrs)
        logger.debug(super().__new__)
        cls = super(ClassProxyMeta, mcs).__new__(mcs, clsname, bases, attrs)
        return cls

    def __getattr__(self, item):
        logger.debug(f'{self}.__getattr__ > {item} in {self}.__dict__ == {item in self.__dict__}')
        if item in self.__dict__:
            return super().__getattr__(item)
        logger.debug('Creating {} proxy object for domain {}'.format(self.__name__, item))
        if self.__name__ == 'www':
            url = '{}://www.{}'.format('https' if self.https_default else 'http', item)
        else:
            url = '{}://{}'.format(self.__name__, item)
        instance = self(url)
        return instance

    def __repr__(self) -> str:
        return 'ClassProxy(class={})'.format(self.__name__)


class www(metaclass=ClassProxyMeta):
    url: str
    https_default: bool = False

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
        task_name: str = 'www.Future({} -> {})'.format(self.url, self.method)
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

    await div_test()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(test())
