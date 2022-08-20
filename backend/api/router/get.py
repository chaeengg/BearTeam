from PIL import Image
from pathlib import Path
from collections import defaultdict
from fastapi import Response
import io
import re
import json
import numpy as np
import base64
from pydantic import BaseModel
from pydantic import ValidationError


url = {
    'assets': Path('assets'),
}

@app.get('/service/image/')
async def read_all_images():
    files = []
    for assetUrl in url['assets'].iterdir():
        asset = str(assetUrl).split('/')[-1]
        img = Image.open(assetUrl)
        with io.BytesIO() as buf:
            img.save(buf, format='png')
            im_bytes = buf.getvalue()
            file = (asset, base64.b64encode(im_bytes))
            files.append(file)
    return files

@app.get('/service/image/real-time')
async def read_image():
    pass

@app.get('/service/annotation/')
async def read_all_annotations():
    files = []
    pass

@app.get('/service/annotation/real-time')
async def read_annotation():
    pass

