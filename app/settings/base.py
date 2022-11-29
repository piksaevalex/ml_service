from pathlib import Path
from pydantic import BaseSettings


BASE_DIRECTORY = Path(__file__).absolute().parent.parent.parent


class AdvancedBaseSettings(BaseSettings):
    class Config:
        allow_mutation = False
