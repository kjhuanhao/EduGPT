# -*- coding:utf-8 -*-
# @File      : bili_subtitle_downloader.py
# @Time      : 2023/7/18
# @Author    : LinZiHao
# @Desc      : bili字幕下载模块
import time

import requests
import re
from exceptions.subtitle_download_exception import SubTitleDownloadException
from bilibili_api import sync, video
from loguru import logger
from common.config import Config


def _extract_bv_number(url):
    pattern = r'BV([A-Za-z0-9]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(0)
    else:
        return None


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
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        'Host': 'api.bilibili.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    }
    _PAGE_LIST_URL = 'https://api.bilibili.com/x/player/pagelist'
    _SUBTITLE_URL = f'https://api.bilibili.com/x/player/v2'

    def __init__(self,
                 link: str,
                 p_num: str,
                 ) -> None:
        """
        :param link:视频链接
        :param p_num:分集号
        """
        self.bv_id = _extract_bv_number(link)
        self.p_num = int(p_num)
        self.cookie = {'SESSDATA': Config.get_SESSDATA()}
        # if self.cookie is None:
        #     logger.warning("cookie是空的")
        #     raise CookieMissingException("cookie不存在")

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

    def download_subtitle(self) -> str:
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
        # headers = self._HEADERS.copy()  # 复制_HEADERS字典
        # headers['Cookie'] = "; ".join(f"{key}={value}" for key, value in self.cookie.items())  # 将cookie添加到headers
        time.sleep(3)
        response = requests.get(self._SUBTITLE_URL, headers=self._HEADERS, params=params, cookies=self.cookie)
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
