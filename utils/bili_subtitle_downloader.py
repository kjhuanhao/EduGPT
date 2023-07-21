# -*- coding:utf-8 -*-
# @File      : bili_subtitle_downloader.py
# @Time      : 2023/7/18
# @Author    : LinZiHao
# @Desc      : bili字幕下载模块

import requests
import os
from typing import List
from dotenv import load_dotenv, find_dotenv
from exceptions.subtitle_download_exception import SubTitleDownloadException
from exceptions.cookie_missing_exception import CookieMissingException
from bilibili_api import sync, video
from loguru import logger

load_dotenv(find_dotenv(), override=True)


class BiliSubtitleDownloader:
    """
    下载B站字幕
    Example:
            bv_id = 'BV1ps4y1m75J'  # 替换为视频的 BV 号
            p_num = 0  # 替换为视频的分集号，从 0 开始

            downloader = BiliSubtitleDownloader(bv_id, p_num)
            subtitle = downloader.download_subtitle()
            print(f'CC 字幕内容: {subtitle}')
    """
    _HEADERS = {
        'authority': 'api.bilibili.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'origin': 'https://www.bilibili.com',
        'referer': 'https://www.bilibili.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    }
    _PAGE_LIST_URL = 'https://api.bilibili.com/x/player/pagelist'
    _SUBTITLE_URL = f'https://api.bilibili.com/x/player/v2'

    # TODO cookie有问题
    def __init__(self,
                 bv_id: str,
                 p_num: str,
                 ) -> None:
        """
        :param bv_id:视频的 BV 号
        :param p_num:分集号
        """
        self.bv_id = bv_id
        self.p_num = int(p_num)
        self.cookie = {'SESSDATA': os.getenv("SESSDATA")}
        if self.cookie is None:
            logger.warning("cookie是空的")
            raise CookieMissingException("cookie不存在")

    def get_bili_info(self) -> dict:
        return {"bv_id": self.bv_id,
                "cid": self._get_cid(),
                "title": self._download_title()}

    def _download_title(self) -> str:
        """
        下载标题
        :return:标题
        """
        v = video.Video(f'{self.bv_id}')
        info = sync(v.get_info())
        title = info['title']
        logger.info("成功获取标题")
        return title

    def _download_subtitle(self) -> str:
        """
        清洗subtitle_url页面内容
        :return: subtitle
        """
        subtitle_list = self._get_subtitle_url(self._get_cid())
        subtitle = ", ".join([x['content'] for x in subtitle_list])
        logger.info("成功获取字幕")
        return subtitle

    def _get_cid(self):
        """
        获取cid；若为合集视频，则获取p_num指定的cid
        :return: cid
        """
        logger.info("发送请求获取视频的cid")
        response = requests.get(self._PAGE_LIST_URL, params={'bvid': self.bv_id}, headers=self._HEADERS)
        # print(response.json())
        cid = [x['cid'] for x in response.json()['data']][self.p_num]
        logger.info("成功获取视频的cid")
        # print(cid)
        return cid

    def _get_subtitle_url(self, cid: int):
        """
        发送请求获取subtitle_url
        :param cid: cid
        :return: subtitle_url
        """
        logger.info("发送请求获取subtitle_url")
        params = (
            ('bvid', self.bv_id),
            ('cid', cid)
        )
        headers = self._HEADERS.copy()  # 复制_HEADERS字典
        headers['Cookie'] = "; ".join(f"{key}={value}" for key, value in self.cookie.items())  # 将cookie添加到headers
        response = requests.get(self._SUBTITLE_URL, headers=headers, params=params)
        subtitles = response.json()['data']['subtitle']['subtitles']
        if subtitles:
            subtitles = ['https:' + sub['subtitle_url'] for sub in subtitles]
            # print(subtitles)
            logger.info("成功获取subtitle_url")
            return self._request_subtitle_url_content(subtitles[0])
        raise SubTitleDownloadException("字幕下载失败，请确保原视频有cc字幕并更换新的cookie")

    @staticmethod
    def _request_subtitle_url_content(url: str):
        logger.info("发送请求获取subtitle_url页面内容")
        response = requests.get(url)
        if response.status_code == 200:
            logger.info("成功获取subtitle_url页面内容")
            body = response.json()['body']
            # print(body)
            return body
        raise SubTitleDownloadException("请求获取subtitle_url页面内容失败，请确保网络良好")


if __name__ == '__main__':
    b = BiliSubtitleDownloader("BV1qW4y1a7fU", "0")._download_subtitle()
    print(b)
