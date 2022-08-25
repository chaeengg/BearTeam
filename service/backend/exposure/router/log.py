from fastapi import APIRouter, Response
from datetime import datetime

from common.types import *
from model.utils.mymodel import MyModel

model = MyModel()

router = APIRouter(prefix='/log', tags=['log'],)

@router.post('/{title}/start', response_model=Video)
async def start_video(title, response:Response):
    """
    카메라는 계속 사진을 찍고 있도록 만든다.
    """
    global videos
    videos = await camera.get_videos()

    if title not in videos:
        videos[title] = await camera.start_video(title, 640, 640)

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

@router.post('/{title}/checkpoint', response_model=boolean)
async def make_checkpoint(title, response:Response):
    """
    Save latest frame for logging
    """
    global videos
    if title not in videos or len(videos[title].frames) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return None
    else:
        return await camera.save_frame(videos[title], videos[title].frames[-1])


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
        img:Image = await camera.capture(videos[title])
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