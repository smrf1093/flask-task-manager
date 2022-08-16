from apps.users.models import User
from functools import wraps
from flask import request, jsonify
import jwt
# TODO: app configuration can be used here 
from .constants import token_salt


# decorator code
def class_route(self, rule, endpoint, **options):
    """
    This decorator allow add routed to class view.
    :param self: any flask object that have `add_url_rule` method.
    :param rule: flask url rule.
    :param endpoint: endpoint name
    """

    def decorator(cls):
        self.add_url_rule(rule, view_func=cls.as_view(endpoint), **options)
        return cls

    return decorator


# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
        # return 401 if token is not passed
        if not token:
            return jsonify({"message": "Token is missing !!"}), 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, token_salt, algorithms=['HS256'])
            current_user = User.query.filter_by(public_id=data["public_id"]).first()
        except Exception:
            return jsonify({"message": "Token is invalid !!"}), 401
        # returns the current logged in users contex to the routes
        kwargs["user"] = current_user
        return f(*args, **kwargs)

    return decorated
