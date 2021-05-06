# -*- coding: utf-8 -*-

"""
Port of proxy-www in npm ()
~~~~~~~~~~~~~~~~~~~
:copyright: (c) 2020 Lapis0875
:license: MIT, see LICENSE for more details.
"""

__title__ = 'proxy_www'
__author__ = 'Lapis0875'
__license__ = 'MIT'
__copyright__ = 'Copyright 2020 Lapis0875'
__version__ = '1.0.0'

from .proxy import www, http, https
from .method import HTTPMethod,\
    GET, HEAD, POST, PUT,\
    DELETE, CONNECT, OPTIONS, TRACE, PATCH

__all__ = (
    'www', 'http', 'https',
    'HTTPMethod',
    'GET', 'HEAD', 'POST', 'PUT',
    'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH',
)
