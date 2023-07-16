# -*- coding:utf-8 -*-
# @FileName  : plot_exception.py
# @Time      : 2023/7/16
# @Author    : LaiJiahao
# @Desc      : None

class PlotException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)