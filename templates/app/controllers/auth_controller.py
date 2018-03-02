from flask import Blueprint, g, session, request, redirect
from library.engine.utils import json_response


class AuthController(Blueprint):
    def __init__(self, *args, **kwargs):
        self.require_auth = kwargs.get("require_auth") or False
        if "require_auth" in kwargs:
            del(kwargs["require_auth"])
        Blueprint.__init__(self, *args, **kwargs)
        self.before_request(self.set_current_user)

    @staticmethod
    def _get_user_from_authorization_header():
        if "Authorization" in request.headers:
            auth = request.headers["Authorization"].split()
            if len(auth) == 2 and auth[0] == "Token":
                from app.models import Token
                token = Token.find_one({ "token": auth[1] })
                if token is not None and not token.expired:
                    return token.user
        return None

    @staticmethod
    def _get_user_from_session():
        from app.models import User
        user_id = session.get("user_id")
        if user_id:
            user = User.find_one({"_id": user_id})
            return user


    @staticmethod
    def _get_user_from_x_api_auth_token():
        if "X-Api-Auth-Token" in request.headers:
            from app.models import Token
            token = Token.find_one({ "token": request.headers["X-Api-Auth-Token"] })
            if token is not None and not token.expired:
                return token.user
            else:
                return None

    def set_current_user(self):
        g.user = self._get_user_from_session() or \
                    self._get_user_from_x_api_auth_token() or \
                    self._get_user_from_authorization_header()
        if g.user is None and self.require_auth:
            return self.error_response()

    @staticmethod
    def error_response():
        from app import app
        response = {
            "errors": ["You must be authenticated first"],
            "state": "logged out",
            "auth_url": app.authorizer.get_authentication_url()
        }
        if hasattr(app.authorizer, "NAME"):
            response["auth_text"] = app.authorizer.NAME
        else:
            response["auth_text"] = "external auth"
        return json_response(response, 403)
