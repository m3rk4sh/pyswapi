import asyncio
import httpx


class SWError(Exception):
	def __init__(self, message: str | None = ""):
		self.message = message
		super().__init__(message)

class BaseAPI:

	def __init__(self, token: str, base_url: str):
		self.TOKEN = token
		self.BASE_URL = base_url
		self.__lock = asyncio.Lock()
		self.__headers = {
			"accept": "application/json",
			"api-key": self.TOKEN
		}

	async def _make_request(
		self,
		method: str,
		url: str,
		params: dict | None = {}
	) -> dict:
		async with self.__lock:
			async with httpx.AsyncClient() as client:
				response = await client.request(
					method,
					self.BASE_URL + url,
					params=params,
					headers=self.__headers
				)

			if isinstance(response.json(), dict):
				if response.json().get('detail'):
					raise SWError(response.json().get('detail'))

			return response.json()
