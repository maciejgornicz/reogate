
from contextlib import asynccontextmanager
from reogate.modules import logger
from reogate.modules import settings
from reogate.models.camera import Camera
from fastapi import FastAPI, Request

cameras: dict[Camera] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    for camera_settings in settings.cameras:
        logger.info(f"[{camera_settings.name}] Creating camera")
        model = {**camera_settings.model_dump()}
        cam = await Camera(**model)
        cameras[cam._api.mac_address.replace(":", "").lower()] = cam
        print(cameras)
    yield
    for mac, camera in cameras.items():
        await camera.close()

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    for mac, cam in cameras.items():
        print(cam._api.subscribed())
        await cam._api.subscribe(cam._webhook_url)
    return {"message": "Hello World"}


@app.post("/")
async def webhook(request: Request):
    # for mac, camera in cameras.items():
    #     print(camera._api.subscribed())
    print(await request.body())
    return {"status": "ok"}
