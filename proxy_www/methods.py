import typing
from .implementation import www, http, https


def __httpmethod__class_getitem__(cls, proxy_obj: typing.Union[www, http, https]):
    proxy_obj.method = cls.__name__
    return proxy_obj


class GET:
    __class_getitem__ = __httpmethod__class_getitem__


class HEAD:
    __class_getitem__ = __httpmethod__class_getitem__


class POST:
    __class_getitem__ = __httpmethod__class_getitem__


class PUT:
    __class_getitem__ = __httpmethod__class_getitem__


class DELETE:
    __class_getitem__ = __httpmethod__class_getitem__


class CONNECT:
    __class_getitem__ = __httpmethod__class_getitem__


class OPTIONS:
    __class_getitem__ = __httpmethod__class_getitem__


class TRACE:
    __class_getitem__ = __httpmethod__class_getitem__


class PATCH:
    __class_getitem__ = __httpmethod__class_getitem__
