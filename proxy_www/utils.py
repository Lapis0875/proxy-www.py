import logging
import sys
from typing import Callable, Any

DEBUG = logging.DEBUG
INFO = logging.INFO


def wrap_class_method(clsname: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func.__qualname__ = f'{clsname}.{func.__name__}'
        return func
    return decorator


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger('proxy_www')
    if len(logger.handlers) > 0:
        return logger
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter(
            style='{',
            fmt='[{asctime}] [{levelname}] {name}: {message}'
        )
    )
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger


def test():
    class MonkeyMeta(type):
        def __new__(mcs, clsname, bases, attrs):
            original_init = attrs.get('__init__')
            if original_init is not None:
                @wrap_class_method(clsname)
                def __init__(self):
                    print(f"Monkey Patching for class {clsname} success")
                    print(f'Original class {clsname} defined original __init__ : Calling')

                    original_init(self)
            else:
                @wrap_class_method(clsname)
                def __init__(self):
                    print(f"Monkey Patching for class {clsname} success")
                    print(f'Original class {clsname} not defined original __init__ : Ignoring')

            @wrap_class_method(clsname)
            def __repr__(self):
                return f'PY_CLASS(name={clsname})#PATCHED'

            attrs.update({
                __init__.__name__: __init__,
                __repr__.__name__: __repr__
            })

            cls = super().__new__(mcs, clsname, bases, attrs)

            print(original_init)
            print(__init__)
            print(cls.__init__)
            return cls

    class A(metaclass=MonkeyMeta):
        def __init__(self):
            print("HELLO! I'm class A!")

        def __repr__(self):
            return 'PY_CLASS(name=A)'

    class B(metaclass=MonkeyMeta):
        def __repr__(self):
            return 'PY_CLASS(name=B)'

    a = A()
    print(f'{a!r}')
    b = B()
    print(f'{b!r}')


if __name__ == '__main__':
    test()
