# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/5/17 10:57
from collections import Iterable

from sqlalchemy import text

from ihome.wsgi import db


def sort_queryset(model,sort_list,sort_field='id'):
    """
    自定义排序
    :param model:模型类
    :param sort_list: 预先要组成的顺序列表
    :param sort_field: 默认排序依据字段
    :return: 已经排好序的List
    """
    assert isinstance(sort_field,Iterable),(
        f'传入的sort_list,{sort_list},不是可迭代对象'
    )
    assert hasattr(model,sort_field),(
        f'`{model}`模型类没有`{sort_field}`属性!'
    )

    sku_ids = ','.join([str(i) for i in sort_list])
    field_sql = f"FIELD(`{sort_field}`,{sku_ids}) as field_sql"

    model_attr=getattr(model,sort_field)
    query=db.session.query(model, field_sql).filter(model_attr.in_(sort_list)).order_by(
        text('field_sql')).all()
    return [i[0] for i in query]
