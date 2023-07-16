# -*- coding:utf-8 -*-
# @FileName  : cache_handler.py
# @Time      : 2023/7/16
# @Author    : LaiJiahao
# @Desc      : 缓存处理

import os
import json

from loguru import logger
from typing import Dict


class CacheHandler:
    _OUTPUT_FILE = "/cache/output.json"

    def __init__(self):
        pass

    def output_cache(self, response: Dict) -> None:
        """
        将输出后的内容进行本地缓存
        :param response: 响应的结果，需要提前封装为dict
        :return: None
        """
        logger.info("正在缓存输出信息")
        if not os.path.exists("/cache"):
            os.mkdir("cache")

        if os.path.isfile(self._OUTPUT_FILE):
            with open(self._OUTPUT_FILE, 'r') as f:
                existing_data = json.load(f)
        else:
            existing_data = []
        existing_data.append(response)

        with open(self._OUTPUT_FILE, 'w') as f:
            json.dump(existing_data, f)

        logger.info("缓存结束")
