# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/5/8 10:14
from importlib import import_module
from collections import Iterable

def import_string(dotted_path):
    """
    给出字符串路径,加载该模块
    :param dotted_path: 字符串路径
    :return: 模块
    """
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError as err:
        raise ImportError(f"{dotted_path}:不是一个module路径" % dotted_path) from err

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError as err:
        raise ImportError(f'Module {module_path} 没有找到 {class_name} 属性/类' ) \
            from err


def model_to_dict(result):
    # 转换完成后，删除  '_sa_instance_state' 特殊属性
    try:
        if isinstance(result, Iterable):
            tmp = [dict(zip(res.__dict__.keys(), str(res.__dict__.values()))) for res in result]
            for t in tmp:
                t.pop('_sa_instance_state')
        else:
            tmp = dict(zip(result.__dict__.keys(), result.__dict__.values()))
            tmp.pop('_sa_instance_state')
        return tmp
    except BaseException as e:
        print(e.args)
        raise TypeError('Type error of parameter')
