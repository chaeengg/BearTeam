from fastapi import APIRouter
from socket import Receiver

router = APIRouter(prefix='/image', tags=['image'])

@router.get('/')
async def get_root():
    """
    Camera 경로에서 모델 가져오기
    """

