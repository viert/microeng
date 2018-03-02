from library.engine.utils import json_response


class ApiError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        data = {
            "error": self.message
        }
        if self.payload:
            data["data"] = self.payload
        return data

    def __repr__(self):
        return "%s: %s, status_code=%s" % (self.__class__.__name__, self.message, self.status_code)

    def __str__(self):
        return "%s, status_code=%s" % (self.message, self.status_code)


class NotFound(ApiError):
    status_code = 404


class Conflict(ApiError):
    status_code = 409


class AuthenticationError(ApiError):
    status_code = 403


def handle_api_error(error):
    return json_response(error.to_dict(), error.status_code)


def handle_other_errors(error):
    return json_response({ "error": str(error) }, 400)