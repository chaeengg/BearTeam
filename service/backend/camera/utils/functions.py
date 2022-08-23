from common.types import *
from ..assets import storeConfig

import io
import base64
from pathlib import Path
from PIL import Image as PILImage

async def make_frame_name(video:Video, frame_id:int)->str:
    return storeConfig['paths']['frames'] / video.title / (str(frame_id) + '.' + video.format)


async def make_bytes_from_img(img:PILImage):
    buf = io.BytesIO()
    img.save(buf, format='JPEG')
    bytesImg = buf.getvalue()

    bytesImg = base64.b64encode(bytesImg)
    return bytesImg