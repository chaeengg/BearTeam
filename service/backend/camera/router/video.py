from common.types import *
from assets import storeConfig

import json
from fastapi import APIRouter, Response, status

router = APIRouter(prefix='/video', tags=['video'])



@router.get('/', response_model=Video)
async def get_root(response:Response):
    """
    Return default Video info
    """
    videoPath = storeConfig['paths']['videos'] / 'default.json'
    if not videoPath.exists():
        response.status_code = status.HTTP_404_NOT_FOUND
        return None

    with open(videoPath) as fd:
        video = json.load(fd)
        return Video(**video)