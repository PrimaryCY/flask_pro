# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/5/11 22:08
from functools import wraps

from flask import session,g

from utils.response_code import RET


def authentication(view):
    @wraps(view)
    def wrap(*args,**kwargs):
        g.user_id=session.get('id')

        if g.user_id:
            return view(*args,**kwargs)
        return {'errno':RET.SESSIONERR,'msg':'用户未登录'}
    return wrap

