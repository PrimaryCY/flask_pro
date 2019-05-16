# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/5/10 21:35
import random
import unittest

from test.test_package.base import Test


class ImageCodeCase(Test):

    def test_image_code(self):
        random_num=random.randint(10000,99990)
        res=self.client.get(f'/{self.app.config["API_URL_VERSION"]}/image_codes/{random_num}')

        self.assertEqual(res.headers['Content-Type'],'image/jpg',(
            f'接口返回错误\n{res.headers}'
        ))


if __name__ == '__main__':
    unittest.main()