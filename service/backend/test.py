from common.types import Object, Image, ObjectCategory, RiskCategory, Log
from datetime import datetime

from typing import List
########################

obj = Object(category=ObjectCategory.BICYCLE, probability=0.7, center=[0.3, 0.2], width=0.1, height=0.2, risk=None)
obj = Object(category=ObjectCategory.BICYCLE, probability=0.7, center=[0.3, 0.2], width=0.1, height=0.2, risk=None)
obj = Object(category=ObjectCategory.BICYCLE, probability=0.7, center=[0.3, 0.2], width=0.1, height=0.2, risk=None)


### Log 찍기
log = Log(recorded=datetime.now(), objects=[], risked=[], risk=RiskCategory.HIGH) # <--- get_grad => 다가오면 risk 

###1. IOU => 같은 오브젝트인지 판단하기
def get_iou(obj1:Object, obj2:Object):
    """
    1. center로 간 좌표를 이렇게 가공하기
    obj1 : x_min, y_min, x_max, y_max
    obj2 : x_min, y_min, x_max, y_max

    2. 
    """
    x_min = obj.center[0] - obj.width * 0.5
    x_max = obj.center[0] + obj.width * 0.5



    return 0.8

def getIOU(box1, box2):
    """
    box : [center_x, center_y, w, h]
    """
    x, y, w, h = box1
    box1_x_min = x - 0.5 * w
    box1_x_max = x + 0.5 * w
    box1_y_min = y - 0.5 * h
    box1_y_max = y + 0.5 * h
    
    x, y, w, h = box2
    box2_x_min = x - 0.5 * w
    box2_x_max = x + 0.5 * w
    box2_y_min = y - 0.5 * h
    box2_y_max = y + 0.5 * h
    
    intersection_x_min = max(box1_x_min, box2_x_min)
    intersection_x_max = min(box1_x_max, box2_x_max)
    intersection_y_min = max(box1_y_min, box2_y_min)
    intersection_y_max = min(box1_y_max, box2_y_max)
    
    intersection_w = intersection_x_max - intersection_x_min + 1
    intersection_h = intersection_y_max - intersection_y_min + 1
    
    # 겹치는지 판단하기
    if intersection_w > 0 and intersection_h > 0:
        intersectionArea = intersection_w * intersection_h
        box1Area = box1[2] * box1[3]
        box2Area = box2[2] * box2[3]
        unionArea = box1Area + box2Area - intersectionArea
        return intersectionArea / unionArea
    else:
        return 0.0 # 겹치지 않으면, 0!


def is_same_object(obj1:Object, obj2:Object, thresh = 0.5):
    ##1. iou 구하기
    if get_iou(obj1, obj2) > thresh:
        return True
    else:
        return False



###2. 크기 + gard => 위험도 판단하기
def determine_risk(obj:Object):
    """
    9등분해서 정하기
    """
    size = obj.width * obj.height # max(size) = 1.0 min(size) = 0.0

    alpha = 0.5
    beta = 1 - alpha

    risk = alpha * size + (1 - alpha) * get_grad(objects) # [0 - 1]

    if risk < 1 / 3:
        return RiskCategory.LOW
    elif risk < 2 / 3:
        return RiskCategory.MID
    else:
        return RiskCategory.HIGH


    if size < 1 / 9:
        return RiskCategory.LOW
    elif size < 2 / 9:
        return RiskCategory.MID
    else:
        return RiskCategory.HIGH


###3. 선형회귀 => 다가오고 있는 물체 판단하기 -> 보류
def get_grad(same_objects:List[Object]):
    """
    프레임 순서로 정렬됨
    [1, 3, 2]
        step 1:(before for statement)
            prv_size = 1
            grad = 0
        
        step 2:(begin for statement)
            prv_size = 1
            cur_size = 3
            grad = alpha * grad + (cur_size - prv_size) = 0 + 2 = 2
        
        step 3:
            prv_size = 3
            cur_size = 2
            grad = alpha * grad + (cur_size - prv_size) = 1.0 * 2 + (-1) = +1.0
    """
    prv_size = obj[0].width * obj[0].height
    grad = 0.0
    alpha = 0.01
    for obj in same_objects[1:]:
        cur_size = obj.width * obj.height
        grad = alpha * grad + (cur_size - prv_size)

        prv_size = cur_size
    
    if grad > 0.03:
        return 1.0
    elif grad < -0.03:
        return 0.0
    else:
        return 0.5



