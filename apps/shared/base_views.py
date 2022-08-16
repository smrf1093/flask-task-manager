from urllib import request
from flask.views import View
from flask import request
from flask_api.exceptions import APIException

class BaseView(View):

    def dispatch_request(self, *args, **kwargs):
        self.response = dict()
        if "user" in kwargs:
            self.user = kwargs["user"]
        if request.method == "POST":
            return self.post()
        if request.method == "GET":
            return self.get()
        if request.method == "DELETE":
            return self.delete()
        if request.method == "PUT":
            return self.put()
        if request.method == "PATCH":
            return self.patch()
        return super().dispatch_request()

    def post(self):
        """ Should be implemented in children """
    
    def get(self):
        """ Should be implemented in children """
    
    def delete(self):
        """ Should be implemented in children """
    
    def put(self):
        """ Should be implemented in children """
    
    def patch(self):
        """ Should be implemented in children """
    
    



