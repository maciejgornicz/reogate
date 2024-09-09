
from contextlib import asynccontextmanager
from reogate.modules import logger
from reogate.modules import settings
from reogate.models.camera import Camera
from fastapi import FastAPI

cameras = []


@asynccontextmanager
async def lifespan(app: FastAPI):
    for camera in settings.cameras:
        logger.info(f"Creating camera {camera.name}")
        cameras.append(await Camera(**camera.model_dump()))
        print(f"Camera {camera.name} created")
    yield
    camera.close()

app = FastAPI(lifespan=lifespan)
