# -*- coding:utf-8 -*-
# @File      : cookie_missing_exception.py
# @Time      : 2023/7/20
# @Author    : LinZiHao
# @Desc      : None

class CookieMissingException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
