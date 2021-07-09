""" 链接格式应为https://xxx/***/****** """
import datetime

from pydantic import BaseModel, Field, HttpUrl

from .base import BaseResponseModel

from extractor import (acfun, baidutieba, bilibili, changya, douyin, haokan,
                       ku6, kuaishou, kugou, kuwo, lizhiFM, lofter, migu_music,
                       momo, music163, open163, pearvideo, pic58, pipigaoxiao,
                       pipix, qianqian, qingshipin, qqmusic, quanminkge,
                       qutoutiao, sing5, sohuTV, ted, tuchong, tudou, weibo,
                       weishi, xiaokaxiu, xinpianchang, zhihu_video,
                       zuiyou_voice)

crawlers = {
    'acfun': acfun,
    'tieba': baidutieba,
    'changya': changya,
    'bili': bilibili,
    'douyin': douyin,
    'haokan': haokan,
    'ku6': ku6,
    'chenzhongtech': kuaishou,
    'kuaishou': kuaishou,
    'kugou': kugou,
    'kuwo': kuwo,
    'lizhi': lizhiFM,
    'lofter': lofter,
    'music.163': music163,
    'open.163': open163,
    'pearvideo': pearvideo,
    'ippzone': pipigaoxiao,
    'pipix': pipix,
    'music.taihe': qianqian,
    'qingshipin': qingshipin,
    'y.qq': qqmusic,
    'kg': quanminkge,
    'qutoutiao': qutoutiao,
    '5sing': sing5,
    'weibo': weibo,
    'weishi': weishi,
    'xiaokaxiu': xiaokaxiu,
    'xinpianchang': xinpianchang,
    'zhihu': zhihu_video,
    'zuiyou': zuiyou_voice,
    'sohu': sohuTV,
    'ted': ted,
    'tudou': tudou,
    'momo': momo,
    'music.migu': migu_music,
    '58pic': pic58,
    'tuchong': tuchong
}


def get_data(url):
    for c_name, c_func in crawlers.items():
        if c_name in url:
            data = c_func.get(url)
            return data
    return None


class RequestModel(BaseModel):
    url: HttpUrl = Field(..., description='单个音频/视频链接地址')


class Result:
    def __init__(self, link, title=None, file_type='unknown'):
        self.title = title or str(datetime.now())
        self.link = link
        self.fileType = file_type

    title: str = None
    link: HttpUrl = None
    fileType: str = None


class ResponseModel(BaseResponseModel):
    data = []


async def process(request: RequestModel) -> ResponseModel:
    data = get_data(request.url)
    if data is None:
        return ResponseModel(ok=False, msg='获取失败')

    title = data.get("title")
    audio_name = data.get("audioName")
    video_name = data.get("videoName")
    author = data.get("author")
    img_list = data.get("imgs")
    audios = data.get("audios")
    videos = data.get("videos")

    results = []
    if img_list:
        result = [Result(img, file_type='jpg') for img in img_list]
        results.extend(result)
    if audios:
        title = (audio_name or "") + "-" + (author or "")
        result = [Result(audio, title, file_type='mp3') for audio in audios]
        results.extend(result)
    if videos:
        title = (video_name or title or "")
        result = [Result(video, title, file_type='mp4') for video in videos]
        results.extend(result)
    return ResponseModel(ok=True, msg='获取成功', data=results)
