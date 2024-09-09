from reolink_aio.api import Host
import asyncio
from reogate.modules import logger


class Camera():
    """ Class for cameras """

    async def __new__(cls, *a, **kw):
        instance = super().__new__(cls)
        await instance.__init__(*a, **kw)
        return instance

    async def __init__(self,
                       name: str,
                       ip: str,
                       username: str,
                       password: str,
                       webhook_url: str,
                       port: int = 80):
        self.name: str = name
        self._ip: str = ip
        self._username: str = username
        self._password: str = password
        self._port: int = port
        self._webhook_url: str = webhook_url
        self._api: Host = Host(self._ip, self._username,
                               self._password, self._port)
        await self._api.get_host_data()
        await self._api.subscribe(self._webhook_url)
        self._renew_task = asyncio.create_task(self._renew_loop())
        logger.info(f"[{self._api.nvr_name}]: Camera created.")

    async def _renew_loop(self):
        logger.info(f"[{self._api.nvr_name}]: Starting renew loop.")
        while True:
            await asyncio.sleep(0.1)
            try:
                if self._api.subscribed and self._api.renewtimer() < 5:
                    self._api.renew()
                    return
                if not self._api.subscribed:
                    self._api.subscribe(self._webhook_url)
            except asyncio.CancelledError:
                break

    async def close(self):
        await self._renew_task.cancel()
        await self._api.logout()
        logger.info(f"[{self._api.nvr_name}]: Camera closed.")
