import sys
from pathlib import Path

if str(Path(__file__).parent.parent) not in sys.path:
    sys.path.append(str(Path(__file__).parent.parent))

from router import video, frame

from fastapi import FastAPI

app = FastAPI()

app.include_router(video.router)
app.include_router(frame.router)