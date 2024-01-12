from sqlalchemy.types import TypeDecorator, String
import json

class JsonEncodedDict(TypeDecorator):
    impl = String

    def process_bind_param(self, value, _):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, _):
        if value is not None:
            value = json.loads(value)
        return value
