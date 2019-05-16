# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/5/9 9:36
import re

from werkzeug.routing import BaseConverter

class ReConverters(BaseConverter):
    """通用正则匹配转换器"""
    def __init__(self,url_map,regix):
        super().__init__(url_map)
        self.regex = regix

    # def to_python(self, value):
    #     value=re.match(self.regex,value)
    #     if value:
    #         return value.groups()
    #     return value