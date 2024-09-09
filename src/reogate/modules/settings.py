from pydantic_settings import BaseSettings
from pydantic import BaseModel
import yaml


class CameraSettings(BaseModel):
    name: str
    ip: str
    port: int
    username: str
    password: str


class Settings(BaseSettings):
    cameras: list[CameraSettings]

    @classmethod
    def from_yaml(cls, file_path: str):
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
        return cls(**data)


settings = Settings.from_yaml('reogate/config/config.yaml')
