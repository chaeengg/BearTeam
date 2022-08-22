from pydanic import BaseModel

class Video(BaseModel):
    width=float
    height=float
    most_danger_obj=List[Object]



class Log(BaseModel):
    bboxs: List[BBOX]
    img_danger: int # 1 - 3
    comming_object: List[int] # object의 index


class Object(BaseModel):
    # center 좌표
    x=float
    y=float
    w=float
    h=float
    obj_danger = int # 1 - 3
    obj_class: string

