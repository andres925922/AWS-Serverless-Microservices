from functools import wraps
from typing import Callable
import logging
import traceback
from ..enums import HttpCodes
from ..utils import build_response

class HttpException(Exception):

    code: int = HttpCodes.INTERNAL_SERVER_ERROR
    
    def __init__(self, message: str, code: int):
        super().__init__(message)
        self.code = code

    @staticmethod
    def throw_http_exception_decorator(logger: logging.Logger) -> Callable:
        """
        Decorator to handle exceptions in a lambda function handler.
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except HttpException as e:
                    logger.error(f"HTTP Exception: {e}", extra={
                        "code": e.code,
                        "caller": func.__name__,
                        "args": args,
                        "kwargs": kwargs,
                        "message": str(e),
                        "traceback": traceback.format_exc(),
                    })
                    return build_response(
                        status_code=e.code,
                        body={
                            "error": str(e),
                        },
                    )
                except Exception as e:
                    logger.error(f"Exception: {e}", extra={
                        "caller": func.__name__,
                        "args": args,
                        "kwargs": kwargs,
                        "message": str(e),
                        "traceback": traceback.format_exc(),
                    })
                    return build_response(
                        status_code=HttpCodes.INTERNAL_SERVER_ERROR,
                        body={
                            "error": str(e),
                        },
                    )
            return wrapper
        return decorator