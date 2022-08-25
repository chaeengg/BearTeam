from common.types import *
from common.utils import *
from ..assets import storeConfig

from .functions import *

import os
import json
import shutil
import subprocess
from datetime import datetime

import numpy as np
import base64

class MyModel(metaclass=Singleton):
    def __init__(self, maxRecord=10):
        """
        maxRecord : 몇 개의 Log를 메모리에 기억하고, 사용할 것인지!
        """
        self._logs:List[Log] = []
        self.maxRecord = maxRecord

    @property
    def logs(self):
        return self._logs

    @property
    def logSrc(self):
        if len(self.logs) == 0:
            return ""
        else:
            return self.logs[0]

    async def add_log(self, log:Log)->None:
        """
        Log가 한계까지 쌓이면 디스크에 저장하고, 가장 오래된 로그를 삭제한다.
        Memory 상에 있는 Log는 항상 같은 Src Video이다!!
        """
        
        if len(self.logs) != 0:
            if self.logs[0].src != log.src:
                await self.save_log(self.logs[0].src, removed=True)
            else:
                await self.save_log(self.logs[0], removed=False)

        if len(self.logs) == self.maxRecord:
            self.logs.pop(0)
        
        self.logs.append(log)
        return None

    async def start_log(self, title) -> Log:
        log = Log(src=title, recorded=datetime.now(), objects=[], risked=[], risk=RiskCategory.LOW)
        
        if (storeConfig["path"]['logs'] / title).exists():
            shutil.rmtree(storeConfig['paths']['logs'] / title)
        os.makedirs(storeConfig['paths']['logs'] / title, exist_ok=False)
        
        await self.add_log(log)

        return log

    async def end_log(self, src:str, savedSrc:str) -> None:
        """
        메모리에 있는 Log들을 모두 저장하고, 메모리를 비운다.
        이후, log의 src를 savedSrc로 바꾼다.
        """
        await self.save_log(src, removed=True)
        subprocess.run(['mv', storeConfig['paths']['logs'] / src, storeConfig['paths']['logs'] / savedSrc])
        return None

    async def save_log(self, src:str, removed=False) -> bool:
        """
        메모리에 있는 Log를 모두 저장한다.
        removed=True라면 Memory를 비운다.
        만약 현재 Log의 src가 지정된 src가 아니라면 False를 반환한다.
        """

        for log in self.logs:
            name = await make_log_name(log.src, log.id)
            with open(name, 'w') as fd:
                fd.write(log.json())

        if removed:
            self._logs = []
        
        if len(self.logs) != 0 and self.logs[0].src != src:
            return False
        else:
            return True


    async def write(self, img:Image)-> Log:
        """
        Model을 돌려 Log를 기록하고 반환하기
        RGBA -> RGB Channel로 변경하여 Model에 넣는다.
        id는 Image의 Id와 동일하다.
        """
        
        data = np.frombuffer(base64.b64decode(img.data)).reshape(img.width, img.height, -1)[..., :3]
        rawCategory, props, cx, cy, w, h = await self._run(data)
        
        category = None
        for c in ObjectCategory:
            if int(c) == rawCategory:
                category = c
                break
        obj = Object(category=category, probability=props, center=[cx, cy], width=w, height=h, risk=RiskCategory.LOW)



        log = Log(img.src, img.id, recorded=datetime.now(), objects=objs, risked=risked, risk=risk)
        
        self.add_log(log)
        return log

    async def _run(self, img:np.ndarray):
        """
        Return [category, props, center_x, center_y, w, h]
        상대좌표!
        """
        return [0.5,0.5,0.5,0.5,0.5,0.5]

    async def get_log(self, src:str, id: int) -> Log:
        """
        1. Memory에 있는 Log인지 확인한다.
        2. Memory에 없다면, 저장된 로그를 불러온다.
           2-1. 불러온 로그를 메모리에 저장하고, src를 검사한다.
        """
        for log in self.logs:
            if log.src == src and log.id == id:
                return log
            else:
                continue
        
        logPath = await make_log_name(src, id)
        if not logPath.exists():
            raise FileNotFoundError
        else:
            with open(logPath, 'r') as fd:
                log = Log(**json.load(fd))
                await self.add_log(log)
                return log

    