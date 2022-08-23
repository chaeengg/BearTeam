from fastapi import APIRouter
from datetime import datetime

from common.types import *


router = APIRouter(prefix='/log', tags=['log'],)

@router.get('/', response_model=Log)
async def get_root():
    """
    Return default log
    """
    return Log(recorded=datetime.now(), objects=[], risked=[], risk=RiskCategory.LOW)

@router.get('/{title}')
async def get_title(title):
    """
    Return a specific log
    """
    return title

@router.get('/streaming')
async def get_stream():
    """
    Return a latest log
    """
    return None