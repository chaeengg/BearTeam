from .category import *

import numpy as np
from pytz import timezone
from datetime import datetime

from pydantic import Extra

class ObjectConfig:
    title = "ObjectSchema"
    schema_extra = {
        "examples": [
            {
                'category'    : 'bicycle, motorcycle, kickboard',
                'probability' : 0.5, 
                'center'      : ['x', 'y'],
                'width'       : '[0.0, 1.0]',
                'height'      :  '[0.0, 1.0',
                'risk'        :  '0: low, 1: mid, 2: high'
            },
        ]
    }


class ImageConfig:
    title = "ImageSchema"
    schema_extra = {
        "examples": [
            {
                'src'      : 'record001',
                'id'       : '1',
                'title'    : 'record001_1.jpeg',
                'captured' : datetime.now(timezone('Asia/Seoul')),
                'width'    : 640,
                'height'   : 640,
                'risked'   : ['object1', 'object2'],

            }
        ]
    }

class LogConfig:
    title = "LogConfig"
    schema_extra = {
        "examples": [
            {
                "recorded": datetime.now(timezone('Asia/Seoul')),
                "objects" : ['object1(risk = 2)', 'object2(risk = 1)', 'object3(risk = 2)'],
                "risked"  : [0, 2],
                "risk"    : "The highest risk in the scene" 
            }
        ]
    }