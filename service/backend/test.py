from common.types import *
from datetime import datetime

obj = Object(category=ObjectCategory.BICYCLE, probability=1.0, center=[.5, .5],width=0.3, height=0.4, risk=RiskCategory.MID)

img = Image(src='video001', id=1, captured=datetime.now(), width=300, height=300, risked=[obj])

log = Log(recorded=datetime.now(), objects=[obj], risked=[], risk=RiskCategory.LOW)
print(log.json())