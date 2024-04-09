import typing
import jinja2
import json


class Converter:

    def __init__(self, node):
        self.node = node

    def bool(self, value: typing.Any):
        if isinstance(value, str):
            if value.lower() == 'true':
                return True
            elif value.lower() == 'false':
                return False
            return bool(eval(self.render(value)))
        return bool(value)

    def float(self, value: typing.Any):
        if isinstance(value, str):
            return eval(self.render(value))
        else:
            return float(value)

    def int(self, value: typing.Any):
        if isinstance(value, str):
            return int(eval(self.render(value)))
        else:
            return int(value)

    def render(self, value: str, context: dict = None) -> str:
        ctx = { }
        if self.node.context is not None:
            ctx.update(self.node.context)
        if self.node.attrs is not None:
            ctx.update(self.node.attrs)
        if context is not None:
            ctx.update(context)
        for key in ctx:
            if callable(ctx[key]):
                ctx[key] = ctx[key]()
        return jinja2.Template(value).render(ctx)

    def list(self, value: typing.Any) -> typing.List[typing.Any]:
        if isinstance(value, str):
            return eval(self.render(value))
        elif isinstance(value, list):
            return value
        elif isinstance(value, tuple):
            return list(value)
        else:
            try:
                import numpy
                if isinstance(value, numpy.ndarray):
                    return value.tolist()
            except ImportError:
                pass
            raise Exception(f'array error {value}')

    def dict(self, value: typing.Any) -> typing.Dict[str, typing.Any]:
        if isinstance(value, str):
            return eval(self.render(value))
        elif isinstance(value, dict):
            return value
        else:
            raise Exception(f'dict error {value}')

    def json_loads(self, value: typing.Any):
        if isinstance(value, str):
            return json.loads(value)
        elif isinstance(value, dict):
            return value
        elif isinstance(value, list):
            return value
        elif isinstance(value, tuple):
            return value
        else:
            try:
                import numpy
                if isinstance(value, numpy.ndarray):
                    return value
            except ImportError:
                pass
            raise Exception(f'json loads error {value}')
