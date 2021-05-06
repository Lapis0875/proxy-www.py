import enum
import sys


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