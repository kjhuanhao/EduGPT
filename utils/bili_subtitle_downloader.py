import requests
import os
from typing import List
from dotenv import load_dotenv, find_dotenv
from exceptions.subtitle_download_exception import SubTitleDownloadException
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
    _HERDERS = {
        'authority': 'api.bilibili.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'origin': 'https://www.bilibili.com',
        'referer': 'https://www.bilibili.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'Cookie': os.getenv("BILIBILI_COOKIE")
    }
    _PAGE_LIST_URL = 'https://api.bilibili.com/x/player/pagelist'
    _SUBTITLE_URL = f'https://api.bilibili.com/x/player/v2'

    def __init__(self,
                 bv_id: str,
                 p_num: int,
                 cookie: str
                 ) -> None:
        """
        :param bv_id:视频的 BV 号
        :param p_num:分集号
        :param cookie: cookie
        """
        self.bv_id = bv_id
        self.p_num = p_num
        self.cookie = cookie
        cookie = os.getenv("BILIBILI_COOKIE")
        if cookie is None:
            logger.warning("cookie是空的")
            return

    def get_bili_info(self) -> dict:
        return {"title": self._download_title(),
                "subtitle": self._download_subtitle()}

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
        下载字幕
        :return: 字幕
        """
        subtitle_list = self._get_subtitle(self._get_player_list()[self.p_num])
        subtitle = ", ".join([x['content'] for x in subtitle_list])
        logger.info("成功获取字幕")
        return subtitle

    def _get_subtitle_list(self, cid: int):
        """
        发送请求获取指定cid的cc字幕列表
        :param cid: cid
        :return: cid
        """
        logger.info("发送请求获取指定cid的cc字幕列表")
        params = (
            ('bvid', self.bv_id),
            ('cid', cid)
        )
        response = requests.get(self._SUBTITLE_URL, headers=self._HERDERS, params=params)
        subtitles = response.json()['data']['subtitle']['subtitles']
        if subtitles:
            return ['https:' + sub['subtitle_url'] for sub in subtitles]
        return []

    def _get_player_list(self) -> List:
        """
        获取分P视频的List
        :return: 分P视频的List
        """
        logger.info("获取分P视频的List")
        response = requests.get(self._PAGE_LIST_URL, params={'bvid': self.bv_id})
        cid_list = [x['cid'] for x in response.json()['data']]
        return cid_list

    def _get_subtitle(self, cid: int):
        """
        获取指定cid的字幕
        :param cid:
        :return: cid
        """
        logger.info("获取指定cid的字幕")
        subtitles = self._get_subtitle_list(cid)
        if subtitles:
            return self._request_subtitle(subtitles[0])
        else:
            cookie = input("请输入cookie：")
            with open("./cookie", "w") as f:
                f.write(cookie)
            self._HERDERS["Cookie"] = self.cookie
            subtitles = self._get_subtitle_list(cid)
            if subtitles:
                return self._request_subtitle(subtitles[0])

        logger.error("字幕下载失败，请确保原视频有cc字幕并更换新的cookie")
        raise SubTitleDownloadException("字幕下载失败，请确保原视频有cc字幕并更换新的cookie")

    @staticmethod
    def _request_subtitle(url: str):
        logger.info("正在发送字幕请求")
        response = requests.get(url)
        if response.status_code == 200:
            body = response.json()['body']
            return body
