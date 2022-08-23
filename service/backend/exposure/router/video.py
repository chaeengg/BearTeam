from common.types import *
from camera.utils.mycamera import MyCamera

from typing import List, Dict

from fastapi import APIRouter, Response, status

router = APIRouter(prefix='/video', tags=['video'])

camera = MyCamera()
videos: Dict[str, Video] = {}

@router.post('/{title}/start', response_model=Video)
async def start_video(title, response:Response):
    """
    카메라는 계속 사진을 찍고 있도록 만든다.
    """
    global videos
    videos = await camera.get_videos()

    if title not in videos:
        videos[title] = await camera.start_video(title, 300, 300)

    return videos[title]


@router.post('/{title}/end', response_model=Video)
async def end_video(title, response:Response):
    global videos
    if title not in videos:
        response.status_code = status.HTTP_404_NOT_FOUND
        return None
    else:
        videos[title] = await camera.end_video(videos[title]) # duration update
        return videos[title]

@router.get('/{title}/streaming', response_model=Image)
async def get_stream(title:str, response:Response):
    """
    Take a picture
    모델을 돌려서 bbox 예측도 필요!
    """
    global videos
    if title not in videos.keys():
        response.status_code = status.HTTP_404_NOT_FOUND
        return None
    else:
        img:Image = await camera.take_picture(videos[title])
        videos[title].frames.append(img)
        return img


@router.get('/{title}/{frame_id}', response_model=Image)
async def get_an_image(title, frame_id:int, response:Response):
    """
    Return a specific image
    """
    global videos
    if title not in videos.keys() or int(frame_id) < 0 or int(frame_id) >= len(videos[title].frames):
        response.status_code = status.HTTP_404_NOT_FOUND
        return None
    else:
        img:Image = await camera.get_frame(videos[title], frame_id)
        videos[title].frames.append(img)
        return img
