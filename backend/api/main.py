from router import *

from fastapi import FastAPI
import json
import os


assert os.path.exists('config.json')

with open('config.json', fd):
    config = json.load(fd)
    app = FastAPI()

    getRouter = GetRouter(app, config)
    postRouter = PostRouter(app, config)

    getRouter()
    postRouter()