from .config import *
from .category import *

import base64
from typing import List, Tuple, Optional, Dict
from pydantic import root_validator, validator, Field, BaseModel
from pydantic.dataclasses import dataclass

from pytz import timezone
from datetime import datetime

"""
datetime이 Json serialize 될 때, bottleneck이 발생한다(5-6 secs)
datetime을 받는 날짜 형식을 str 형식으로 바꾸어 이 현상을 완화한다(1-2 secs)
"""

# @dataclass(config=ObjectConfig)
class Object(BaseModel):
    """
    Detectable Object Model
    All values are relative coordinates nomalized in [0.0, 1.0]
    Probability is the probs of predction
    """
    category: ObjectCategory
    probability: float
    center: Tuple[float, float]
    width : float
    height: float
    risk  : RiskCategory 

    @validator('width', 'height', 'probability', 'center', each_item=True)
    def check_size(cls, v):
        if v < 0.0 or v > 1.0:
            raise ValueError("Unnormalized values")
        else:
            return v

    class Config:
        title = "ObjectSchema"
        schema_extra = {
            "example":
                {
                    'category'    : 'bicycle, motorcycle, kickboard',
                    'probability' : 0.5, 
                    'center'      : ['x', 'y'],
                    'width'       : '[0.0, 1.0]',
                    'height'      :  '[0.0, 1.0',
                    'risk'        :  '0: low, 1: mid, 2: high'
                },
        }

# @dataclass(config=ImageConfig)
class Image(BaseModel):
    """
    src is the name of video(also unique!) \n
    id is an unique value in each video \n
    title is an unique file name formatted like src_id.jpeg \n
    data is the unnormalized image array
    captured is captured time(time-zone is Asia/Seoul) \n
    Width and Height are the number of pixels \n
    Risked are the highest risked objects \n
    """
    captured: datetime
    width: int
    height: int
    risked: List[Object]

    src: str
    id: int
    data: bytes
    title: Optional[str] = None

    @root_validator(pre = True)
    def set_title(cls, vals):
        src, id = vals.get('src'), vals.get('id')
        vals['title'] = src + '_' + str(id) + '.jpeg'
        return vals

    @validator('captured')
    def check_tz(cls, v:datetime):
        KST = timezone('Asia/Seoul')
        return v.astimezone(KST)

    class Config:
        title = "ImageSchema"
        schema_extra = {
            "example":
                {
                    'src'      : 'record001',
                    'id'       : '1',
                    'title'    : 'record001_1.jpeg',
                    'captured' : datetime.now(timezone('Asia/Seoul')),
                    'width'    : 640,
                    'height'   : 640,
                    'risked'   : ['object1', 'object2'],
                    "data"     : "3-channel Image Array [0 - 255] channel values",

                },
        }

# @dataclass(config=LogConfig)
class Log(BaseModel):
    """
    Src is the associated video \n
    id is an unique value in each video \n
    Recorded is a recorded time \n
    Objects are all tracked objects \n
    Risked are the highest riskable objects's indice \n
    Risk is a total risk of the scene
    """
    src: str 
    id: int
    recorded: datetime
    objects: List[Object]
    risked: List[int]
    risk: RiskCategory

    @validator('recorded')
    def check_tz(cls, v:datetime):
        KST = timezone('Asia/Seoul')
        return v.astimezone(KST)

    class Config:
        title = "LogSchema"
        schema_extra = {
            "example": 
                {
                    "src"     : "BearTeam",
                    "id"      : 0,
                    "recorded": datetime.now(timezone('Asia/Seoul')),
                    "objects" : ['object1(risk = 2)', 'object2(risk = 1)', 'object3(risk = 2)'],
                    "risked"  : [0, 2],
                    "risk"    : "The highest risk in the scene" 
                },
        }

# @dataclass(config=FrameConfig)
class Frame(BaseModel):
    """
    Raw Video Frame Type
    """
    id       : int = Field(..., description="Unique Frame Number")
    captured : datetime = Field(..., description="Captured time")

    @validator('captured')
    def check_tz(cls, v:datetime):
        KST = timezone('Asia/Seoul')
        return v.astimezone(KST)

    class Config:
        title = "FrameSchema"
        schema_extra = {
            "example":
                {
                    "id" : 0,
                    "captured": datetime.now(timezone('Asia/Seoul')),
                }
        }

# @dataclass(config=VideoConfig)
class Video(BaseModel):
    """
    Raw Video Annotation Type
    """
    mode       : str = Field(..., description="Image mode like RGB or BGR") 
    title      : str = Field(..., description="video name")
    format     : str = Field(..., description="Image format like jpeg")
    duration   : Dict[str, datetime] = Field(..., description="start and end timestamp")
    
    width      : int = Field(..., description="Frame width")
    height     : int = Field(..., description="Frame height")
    
    frames     : List[Frame] = Field([], description="Video frames")

    @validator('duration')
    def check_duration(cls, v:Dict[str, datetime]):
        if set(v.keys()) != set({'start', 'end'}):
            raise ValueError("duration MUST have only start and end keys")
        
        KST = timezone('Asia/Seoul')
        v['start'] = v['start'].astimezone(KST)
        v['end'] = v['end'].astimezone(KST)

        if v['start'] > v['end']:
            raise ValueError("Start is later than End")

        return v

    class Config:
        title = "VideoConfig"
        schema_extra = {
            "example":
                {
                    "mode"  : "RGB",
                    "title" : "default",
                    "duration" : "{start: start-time, end: end-time}",
                    "width" : 320,
                    "height": 320,
                    "frames": "['frame1', 'frame2', ...]"
                }
        }