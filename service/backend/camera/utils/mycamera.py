from ..assets import storeConfig
from common.types import *

from .functions import make_bytes_from_img, make_frame_name

import base64
import shutil
import os
import subprocess
import numpy as np
import json
from pathlib import Path
from typing import Tuple, Dict
from datetime import datetime
from picamera2 import Picamera2, Preview

from PIL import Image as PILImage

class MyCamera:
    def __init__(self):
        self._camera = Picamera2()
        self._configure_camera()
        self._camera.start()

    def __del__(self):
        """
        video info가 저장되지 않은 frames는 모두 삭제한다.
        """
        self._camera.close()

    def _configure_camera(self):
        self._camera.start_preview(Preview.NULL)
        config = self._camera.create_still_configuration()
        config['buffer_count'] = 5
        self._camera.configure(config)
    
    async def start_video(self, title:str, width:float, height:float)->Video:
        video = Video(mode="RGB", title=title, format="jpeg", duration={"start":datetime.now(), "end":datetime.now()}, width=width, height=height, frames=[])
        if (storeConfig['paths']['frames'] / title).exists():
            shutil.rmtree(storeConfig['paths']['frames'] / title)

        os.makedirs(storeConfig['paths']['frames'] / title)
        return video

        

    async def end_video(self, video:Video) -> Video:
        """
        저장된 파일을 datetime을 덧붙여 새롭게 저장하기
        """
        video.duration["end"] = datetime.now()

        savedTitle = video.title + ':' + '[' + str(video.duration["start"]) + ',' + str(video.duration["end"]) + ']'

        video.title = savedTitle
        subprocess.run(['mv', storeConfig['paths']['frames'] / video.title, storeConfig['paths']['frames'] / savedTitle])
        
        with open(storeConfig['paths']['videos'] / f"{savedTitle}.json", "w") as fd:
            fd.write(video.json())
        return video


    async def take_picture(self, video:Video)->Image:
        """
        사진을 찍고, asset에 저장,
        Image로 반환!
        video 객체 수정은 하지 않는다(호출한 쪽에서 알아서 한당)
        """
        frameId = len(video.frames) + 1
        name = await make_frame_name(video, frameId)
        img:PILImage = self._camera.capture_image().resize([video.width, video.height], PILImage.Resampling.NEAREST)
        img.save(name)
        bytesImg = await make_bytes_from_img(img)
        img.close()
        return Image(captured=datetime.now(), width=video.width, height=video.height, risked=[], src=video.title, id=frameId, data=bytesImg)
        

    async def get_frame(self, video:Video, frame_id: int)->Image:
        imgPath:Path = await make_frame_name(video, frame_id)
        if not imgPath.exists():
            raise FileNotFoundError
        else:
            img = PILImage.open(imgPath).resize([video.width, video.height], PILImage.Resampling.BICUBIC)
            data = make_bytes_from_img(img)
            img.close()
            return Image(captured=video.frames[frame_id].captured, width=video.width, height=video.height, risked=[], src=video.title, id = frame_id, data=data)


    async def get_videos(self)->Dict[str, Video]:
        videos = dict()
        for videoPath in storeConfig['paths']['videos'].iterdir():
            try:
                with open(videoPath, 'r') as fd:
                        video:Video = Video(**json.load(fd))
                        videos[video.title] = video
            except Exception:
                continue
        
        return videos
        