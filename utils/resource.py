# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/5/9 22:12
from flask_restful import Resource, reqparse

from utils.authentication import authentication

class View(Resource):

    method_decorators=[authentication,]

    def __init__(self):
        self.data=reqparse.RequestParser()
        super().__init__()