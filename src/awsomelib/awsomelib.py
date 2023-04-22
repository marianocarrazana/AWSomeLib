import re
from inspect import signature, _empty
from uuid import UUID

from . import state
from .custom_types import GithubHash


class AWSomeApp:
    def __init__(self):
        self.__main = None
        self.__routes = []

    def __call__(self, event, context):
        state.init()
        main_response = self.__main(event, context)
        print(f"{self.__routes=}")
        response = None
        request_route = f"{event['httpMethod']} {event['pathParameters']['proxy']}"
        print(f"{request_route=}")
        for route in self.__routes:
            match = re.search(re.compile(route["route"]), request_route)
            if match:
                print(f"Found route:{route['route']}")
                params = match.groupdict()
                print(f"{params=}")
                sig = signature(route["callback"])
                print(f"{sig=}")
                callback_params = sig.parameters.values()
                print(f"{callback_params=}")
                # print(f"{sig.parameters=}")
                matchs = 0
                for param in callback_params:
                    print(f"{param.annotation=}")
                    print(f"{param.name=}")
                    try:
                        value = match.group(param.name)

                    except IndexError:
                        # Unknown param in function declaration
                        print("--------Index error---------")
                        break
                    except Exception as e:
                        print(e)
                        break
                    value = self.type_converter(value)
                    print(f"{value=}")
                    print(f"{type(value)=}")
                    print(f"{param.annotation==_empty=}")
                    if param.annotation == _empty:
                        is_instance = True
                    else:
                        is_instance = isinstance(value, param.annotation)
                    print(f"{is_instance=}")
                    params[param.name] = value
                    if is_instance:
                        matchs += 1
                print(f"{params=}")
                print(f"{len(callback_params)=} {matchs=}")
                if len(callback_params) == matchs:
                    response = route["callback"](**params)
                    break
        return response or main_response

    def main(self, func):
        self.__main = func

    def get(self, route):
        def decorator(callback):
            self.__add_route("GET", route, callback)
            return

        return decorator

    def post(self, route):
        def decorator(callback):
            self.__add_route("POST", route, callback)
            return

        return decorator

    def put(self, route):
        def decorator(callback):
            self.__add_route("PUT", route, callback)
            return

        return decorator

    def delete(self, route):
        def decorator(callback):
            self.__add_route("DELETE", route, callback)
            return

        return decorator

    def __add_route(self, method: str, route: str, callback):
        regexp = route.replace("/", "/")
        print(f"{regexp=}")
        with_names = re.sub(r"{([^\/:]+)(:[^\/]*)?}", "(?P<\\1>[^\/]+)", regexp)
        final_route = f"^{method} {with_names}$"
        print(f"{final_route=}")
        self.__routes.append({"route": final_route, "callback": callback})

    @staticmethod
    def type_converter(word: str):
        if re.match(r"^(-|\+)?\d+$", word):  # is int
            return int(word)
        elif re.match(r"^(\+|-)?\d*\.\d+$", word):  # is float
            return float(word)
        elif re.match(
            r"^[0-9A-F]{8}-[0-9A-F]{4}-4[0-9A-F]{3}-[89AB][0-9A-F]{3}-[0-9A-F]{12}$",
            word,
            re.IGNORECASE,
        ):  # is a uuid
            return UUID(word)
        try:  # is github hash
            hash_obj = GithubHash(word)
            return hash_obj
        except Exception as e:  # is a string maybe?
            print(e)
            return word
