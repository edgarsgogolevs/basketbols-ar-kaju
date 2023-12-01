from functools import wraps
from flask import request
from marshmallow import ValidationError
import logging

lg = logging.getLogger("modules.validate")


def json(f):
    @wraps(f)
    def wrapper(*args, **kw):
        # JSON validation
        if not hasattr(request, "json_data"):
            try:
                request.json_data = request.get_json(force=True)  # type: ignore
                lg.debug(f"Request JSON {request.json_data}")  # type: ignore
            except Exception as e:
                lg.error(f"JSON validation error: {e}", exc_info=True)
                return {"error": "JSON validation error"}, 400
        return f(*args, **kw)

    return wrapper


def schema(schema):
    """shēma jānorāda formātā fname.SchemaName"""

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):
            if request is None:
                lg.debug("Request is None")
                return f(*args, **kw)
            if request.method == "GET":
                data = dict(request.args)
                view_args = request.view_args
                if view_args:
                    data.update(view_args)
            else:
                data = request.get_json(force=True)
            try:
                schema_obj = schema()
                if not hasattr(request, "parsed"):
                    request.parsed = {}  # type: ignore
                parsed_name = schema.__name__.replace("Schema", "")
                request.parsed[parsed_name] = schema_obj.load(data)  # type: ignore
                lg.debug(f"Parsed {parsed_name} data: {request.parsed[parsed_name]}")  # type: ignore
            except ValidationError as error:
                lg.warning(f"Validation error: {error.messages}")
                return {"error": "Validation error", "fields": error.messages}, 400
            except Exception as e:
                lg.error(f"Schema validation error: {e}", exc_info=True)
                return {"error": "Processing schema validation error"}, 500
            return f(*args, **kw)

        return wrapper

    return decorator
