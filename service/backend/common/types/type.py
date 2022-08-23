from time import time
from .config import *

from typing import List, Tuple, Optional
from pydantic import root_validator, validator
from pydantic.dataclasses import dataclass

from datetime import datetime


@dataclass(config=ObjectConfig)
class Object:
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

@dataclass(config=ImageConfig)
class Image:
    """
    src is the name of video(also unique!)
    id is an unique value in each video
    title is an unique file name formatted like src_id.jpeg
    captured is captured time(time-zone is Asia/Seoul)
    Width and Height are the number of pixels
    Risked are the highest risked objects
    """
    captured: datetime
    width: float
    height: float
    risked: List[Object]

    src: str
    id: int
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

@dataclass(config=LogConfig)
class Log:
    """
    Recorded is a recorded time
    Objects are all tracked objects
    Risked are the highest riskable objects's indice
    Risk is a total risk of the scene
    """
    recorded: datetime
    objects: List[Object]
    risked: List[int]
    risk: RiskCategory

    @validator('recorded')
    def check_tz(cls, v:datetime):
        KST = timezone('Asia/Seoul')
        return v.astimezone(KST)
            

