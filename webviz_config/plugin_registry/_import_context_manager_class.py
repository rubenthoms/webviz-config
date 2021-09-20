import typing
from typing import Callable, Optional, Union, List, Any

# _overloaded_functions_arr: List[Callable] = []
#
# def _custom_overload_decorator_func(func: Callable) -> None:
#    print("Decorator being called")
#    _overloaded_functions_arr.append(func)


# Naming ???
# Naming ???
# Naming ???
# Naming ???
# Capture overloads when importing
# Right now, captures ALL overloads
# Should be limited to init functions


class ImportContextManager:
    def __init__(self) -> None:
        # print('init method called')
        self.overloaded_functions_arr: List[Callable] = []

    def __enter__(self) -> "ImportContextManager":
        # print('enter method called')

        def _inner_custom_overload_decorator_func(func: Callable) -> None:
            # print("Decorator being called")
            self.overloaded_functions_arr.append(func)

        self._old_typing_overload = typing.overload
        typing.overload = _inner_custom_overload_decorator_func

        return self

    def __exit__(self, exc_type: Any, exc_value: Any, exc_traceback: Any) -> None:
        # print('exit method called')
        typing.overload = self._old_typing_overload

    def get_captured_overloads_of_function(self, func: Callable) -> List[Callable]:
        matching_overloads_arr: List[Callable] = []
        for overload in self.overloaded_functions_arr:
            if func.__qualname__ == overload.__qualname__:
                matching_overloads_arr.append(overload)

        return matching_overloads_arr
