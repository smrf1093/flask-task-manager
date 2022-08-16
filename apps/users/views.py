import uuid
import jwt
from datetime import datetime, timedelta
from flask import request, make_response, jsonify
from flask_api import status

from apps.shared.base_views import BaseView
from apps.shared.models import db
from apps.shared.constants import token_salt, ResponseKeys
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User


class RegisterView(BaseView):
    def post(self):
        data = request.form

        role, email = data.get("role"), data.get("email")
        password = data.get("password")

        user = User.query.filter_by(email=email).first()

        if not user:
            user = User(
                public_id=str(uuid.uuid4()),
                roles=role,
                email=email,
                password=generate_password_hash(password),
            )
            db.session.add(user)
            db.session.commit()
            self.response[ResponseKeys.message] = "Successfully registered."
            return make_response(jsonify(self.response), status.HTTP_201_CREATED)
        else:
            self.response[ResponseKeys.message] = "User already exists. Please Log in."
            return make_response(jsonify(self.response), status.HTTP_400_BAD_REQUEST)


class LoginView(BaseView):
    def post(self):
        auth = request.form
        msg_error = "Could not verify"

        if not auth or not auth.get("email") or not auth.get("password"):
            self.response[ResponseKeys.message] = msg_error
            return make_response(
                jsonify(self.response),
                401,
                {"WWW-Authenticate": 'Basic realm ="Login required !!"'},
            )

        user = User.query.filter_by(email=auth.get("email")).first()

        if not user:
            self.response[ResponseKeys.message] = msg_error
            return make_response(
                jsonify(self.response),
                status.HTTP_401_UNAUTHORIZED,
                {"WWW-Authenticate": 'Basic realm ="User does not exist !!"'},
            )

        if not check_password_hash(user.password, auth.get("password")):
            self.response[ResponseKeys.message] = msg_error
            return make_response(
                jsonify(self.response),
                status.HTTP_403_FORBIDDEN,
                {"WWW-Authenticate": 'Basic realm ="Wrong Password !!"'},
            )

        token = jwt.encode(
                {
                    "public_id": user.public_id,
                    "exp": datetime.utcnow() + timedelta(minutes=30),
                },
                token_salt,
            )
        self.response["token"] = token
        return make_response(jsonify(self.response), status.HTTP_200_OK)

