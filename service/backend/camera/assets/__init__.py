from datetime import datetime
from pytz import timezone

from typing import Dict, List
from pydantic import BaseModel, Field, validator

from pathlib import Path

storeConfig = {
    "paths": {
        "videos": Path(__file__).parent / 'videos',
        "frames": Path(__file__).parent / 'frames' 
    }
}

