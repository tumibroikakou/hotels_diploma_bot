import datetime
from functools import wraps
import traceback
from sys import exc_info

from typing import Callable, Any


def logger(func: Callable) -> Callable:
    @wraps(func)
    def wrapped(*args, **kwargs) -> Any:
        func_result = None
        with open('errors.log', 'a', encoding='utf-8') as logfile:
            try:
                func_result = func(*args, **kwargs)
            except Exception:
                logfile.write(f'\n{datetime.datetime.now()} {"-" * 33}\n')
                err_type, err_value, err_traceback = exc_info()
                err = traceback.format_tb(err_traceback)
                tab = '\t'
                logfile. write(f'{tab.join(err)}{err_value}\n{"-" * 60}\n')
        return func_result
    return wrapped
