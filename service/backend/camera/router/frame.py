from common.types import *
from camera.assets import storeConfig

import json
import numpy as np
from PIL import Image as PILImage

from typing import List
from fastapi import APIRouter, Response, status

router = APIRouter(prefix='/frame', tags=['frame'])

@router.get('/{video}', response_model=List[Image])
async def get_all_frames(video: str, response: Response):
    """
    Don't care whether all frames are continuous or not
    Return : [Frames, Height, Width, Channel]
    """
    framePath = storeConfig['paths']['frames'] / 'default'
    videoPath = storeConfig['paths']['videos'] / 'default.json'
    if not videoPath.exists() or not framePath.exists():
        response.status_code = status.HTTP_404_NOT_FOUND
        return None
    
    with open(videoPath, 'r') as fd:
        video:Video = Video(**json.load(fd))
        ret = []
        for frame in video.frames:
            name = await get_frame_name(video, frame)
            img = PILImage.open(framePath / name).resize([video.width, video.height], resample=PILImage.Resampling.BICUBIC)
            data = np.array(img, dtype=np.uint8).tolist()
            img.close()
            ret.append(Image(captured=frame.captured, width=video.width, height=video.height, risked=[], src=video.title, id=frame.id, data=data))
        return ret


@router.get('/{video}/{frame_id}', response_model=Image)
async def get_video_frame(video:str, frame_id:int, response:Response):
    framePath = storeConfig['paths']['frames'] / 'default'
    videoPath = storeConfig['paths']['videos'] / 'default.json'

    if not videoPath.exists() or not framePath.exists():
        response.status_code = status.HTTP_404_NOT_FOUND
        return None

    with open(videoPath, 'r') as fd:
        video:Video = Video(**json.load(fd))
        if frame_id < 0 or frame_id >= len(video.frames):
            response.status_code = status.HTTP_404_NOT_FOUND
            return None

        name = await get_frame_name(video, video.frames[frame_id])   

        if not (framePath / name).exists():
            response.status_code = status.HTTP_404_NOT_FOUND
            return None
        img = PILImage.open(framePath / name).resize([video.width, video.height], resample=PILImage.Resampling.BICUBIC)
        data = np.array(img, dtype=np.uint8).tolist()
        img.close()
        return Image(captured=video.frames[frame_id].captured, width=video.width, height=video.height, risked=[], src=video.title, id=frame_id, data=data)


async def get_frame_name(video:Video, frame:Frame):
    return video.title + '_' + str(frame.id) + '.' + video.format
    










    