from common.types import *
from ..assets import storeConfig

import io
import base64
import numpy as np
from pathlib import Path
from PIL import Image as PILImage

async def make_frame_name(video:Video, frame_id:int)->str:
    return storeConfig['paths']['frames'] / video.title / (str(frame_id) + '.' + video.format)


async def make_bytes_from_img(img:PILImage): 
    bytesImg = np.array(img, dtype=np.uint8).tobytes() # R G B A -> R G B
    bytesImg = base64.b64encode(bytesImg)

    return bytesImg


async def make_img_from_bytes(bytesImg: bytes, width:int, height: int):
    bytesImg = base64.b64decode(bytesImg)
    imgArr = np.frombuffer(bytesImg, dtype=np.uint8).reshape(width, height, -1)
    img = PILImage.fromarray(imgArr)
    return img
