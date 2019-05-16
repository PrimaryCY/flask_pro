# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/5/10 21:30
import random
import unittest
from manage import app, db

from ihome.settings import TestSetting


class Test(unittest.TestCase):

    def setUp(self):
        self.app=app
        TestSetting.init_app(app)
        db.create_all()
        self.client = app.test_client()


    def tearDown(self):
        db.session.remove()
        db.drop_all()


if __name__ == '__main__':

    unittest.main()