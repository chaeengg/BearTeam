from common.types import Object, Image, ObjectCategory, RiskCategory, Log
from datetime import datetime

from typing import List
########################
<<<<<<< HEAD

# 이전 프레임, 현재 프레임.... 프레임 정보는 10초 정도는 보관 -> 10 - 20 정도 디텍션 된 이미지
# Log 1장 = Frame 1장(디텍션된 프레임)
# 제공될 데이터는 Log들!
log1 = Log(recorded=datetime.now(), objects=[], risked=[], risk=RiskCategory.HIGH) # <--- get_grad => 다가오면 risk 
log2 = Log(recorded=datetime.now(), objects=[], risked=[], risk=RiskCategory.HIGH) # <--- get_grad => 다가오면 risk 
log3 = Log(recorded=datetime.now(), objects=[], risked=[], risk=RiskCategory.HIGH) # <--- get_grad => 다가오면 risk 

## 채워야 할 것: risked, risk, object별 risk 

## 1. 같은 오브젝트끼리 묶기 => getIOU => 같은 Object 별 List를 만들기
## 2. risk 계산하기 => size & grad => 가장 최신 Frame의 Object risk에 넣기
## 3. log 전체에 대해서 Risk 계산하기 ==> 가장 큰 Risk 선택하기


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
    y_min = obj.center[1] - obj.width * 0.5
    y_max = obj.center[1] + obj.width * 0.5

    return Object = [x_min, y_min, x_max, y_max]


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

    

###2. 크기 + grad => 위험도 판단하기
def determine_risk(obj:Object):
    """
    9등분해서 정하기
    """
    size = obj.width * obj.height # max(size) = 1.0 min(size) = 0.0

    alpha = 0.5
    beta = 1 - alpha

    risk = alpha * size + (1 - alpha) * get_grad(objects) # [0 - 1]


    if size < 1 / 9:
        return RiskCategory.LOW
    elif size < 2 / 9:
        return RiskCategory.MID
    else:
        return RiskCategory.HIGH
    


    if risk < 1 / 3:
        return RiskCategory.LOW
    elif risk < 2 / 3:
        return RiskCategory.MID
    else:
        return RiskCategory.HIGH



def log_risk(logs):
    
        


    


###3. 변화량만
def get_grad(same_objects:List[Object]):
    """
    프레임 순서로 정렬됨
    [1, 3, 2] version 1
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
            grad = 0.01 * 0.1 + (2-3) = 0.001 -1 = -0.998
            grad = 0.01 * 0.05 + (2-3) = 0.005 -1 = -0.995
    [0.01, 0.03, 0.02, 0.03, 0.06] version 2
        step 1:(before for statement)
            prv_size = 0.01
            grad = 0
        step 2:(begin for statement)
            prv_size = 0.01
            cur_size = 0.03
            grad = alpha * grad + (cur_size - prv_size) = 0 + 0.02 = 0.02
        step 3:
            prv_size = 0.03
            cur_size = 0.02
            grad = alpha * grad + (cur_size - prv_size) = 0.01*0.02 - 0.01 = -0.0098
            
        step 4:
            prv_size = 0.02
            cur_size = 0.03
            grad = alpha * grad + (cur_size - prv_size) = 0.01*(-0.0098) + 0.01 = -0.000098+0.01= 0.0099902
        step 5:
            prv_size = 0.03
            cur_size = 0.06
            grad = alpha * grad + (cur_size - prv_size) = 0.01*(0.0099902) + 0.03 = 0.03xx
    """
    
    prv_size = same_objects[0].width * same_objects[0].height
    grad = 0.0
    alpha = 0.01
    for obj in same_objects[1:]:
        cur_size = obj.width * obj.height
        grad = alpha * grad + (cur_size - prv_size)

        prv_size = cur_size
    
    if grad > 0.01: # threshold : 0.01
        return 1.0
    elif grad < -0.01:
        return 0.0
    else:
        return 0.5
=======

# 이전 프레임, 현재 프레임.... 프레임 정보는 10초 정도는 보관 -> 10 - 20 정도 디텍션 된 이미지
# Log 1장 = Frame 1장(디텍션된 프레임)
# 제공될 데이터는 Log들!
log1 = Log(recorded=datetime.now(), objects=[], risked=[], risk=RiskCategory.HIGH) # <--- get_grad => 다가오면 risk 
log2 = Log(recorded=datetime.now(), objects=[], risked=[], risk=RiskCategory.HIGH) # <--- get_grad => 다가오면 risk 
log3 = Log(recorded=datetime.now(), objects=[], risked=[], risk=RiskCategory.HIGH) # <--- get_grad => 다가오면 risk 

## 채워야 할 것: risked, risk, object별 risk 

## 1. 같은 오브젝트끼리 묶기 => getIOU => 같은 Object 별 List를 만들기
## 2. risk 계산하기 => size & grad => 가장 최신 Frame의 Object risk에 넣기
## 3. log 전체에 대해서 Risk 계산하기 ==> 가장 큰 Risk 선택하기


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


    if size < 1 / 9:
        return RiskCategory.LOW
    elif size < 2 / 9:
        return RiskCategory.MID
    else:
        return RiskCategory.HIGH
    



    if risk < 1 / 3:
        return RiskCategory.LOW
    elif risk < 2 / 3:
        return RiskCategory.MID
    else:
        return RiskCategory.HIGH


###3. 변화량만
def get_grad(same_objects:List[Object]):
    """
    프레임 순서로 정렬됨
    [1, 3, 2] version 1
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
            grad = 0.01 * 0.1 + (2-3) = 0.001 -1 = -0.998
            grad = 0.01 * 0.05 + (2-3) = 0.005 -1 = -0.995

    [0.01, 0.03, 0.02, 0.03, 0.06] version 2
        step 1:(before for statement)
            prv_size = 0.01
            grad = 0

        step 2:(begin for statement)
            prv_size = 0.01
            cur_size = 0.03
            grad = alpha * grad + (cur_size - prv_size) = 0 + 0.02 = 0.02

        step 3:
            prv_size = 0.03
            cur_size = 0.02
            grad = alpha * grad + (cur_size - prv_size) = 0.01*0.02 - 0.01 = -0.0098
            

        step 4:
            prv_size = 0.02
            cur_size = 0.03
            grad = alpha * grad + (cur_size - prv_size) = 0.01*(-0.0098) + 0.01 = -0.000098+0.01= 0.0099902


        step 5:
            prv_size = 0.03
            cur_size = 0.06
            grad = alpha * grad + (cur_size - prv_size) = 0.01*(0.0099902) + 0.03 = 0.03xx

    """
    
    prv_size = same_objects[0].width * same_objects[0].height
    grad = 0.0
    alpha = 0.01
    for obj in same_objects[1:]:
        cur_size = obj.width * obj.height
        grad = alpha * grad + (cur_size - prv_size)

        prv_size = cur_size
    
    if grad > 0.01: # threshold : 0.01
        return 1.0
    elif grad < -0.01:
        return 0.0
    else:
        return 0.5



>>>>>>> eb141b60dfe653b0d8fe1b7f914593b740fda8ce
