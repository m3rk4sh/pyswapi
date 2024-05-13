from .base import BaseAPI
from .types import CoinInfo, Cheque, Invoice, PayHistoryItem
from .const import WAV


class StupidWalletAPI(BaseAPI):

	def __init__(self, token: str):
		super().__init__(token, "https://sw.svat.dev")

	async def get_existing_coins(self) -> list[CoinInfo]:
		"""Returns all realized StupidWallet coins"""
		response = await self._make_request("GET", "/base/existing_coins")
		return [CoinInfo(**data) for data in response]

	async def get_balance(self, coin_id: int = WAV) -> int:
		"""Returns your wallet balance"""
		response = await self._make_request(
			"GET", "/user/get_balance",
			params={
				"coin_id": coin_id
			}
		)
		return response.get("coin_amount")

	async def get_my_cheques(self) -> list[Cheque]:
		"""Returns all your existing Cheques"""
		response = await self._make_request("GET", "/user/my_cheques")
		return [Cheque(**data) for data in response]

	async def get_cheque(self, cheque_id: str) -> Cheque:
		"""Returns Cheque by ID"""
		response = await self._make_request(
			"GET", "/user/info_cheque",
			params={
				"cheque_id": cheque_id
			}
		)
		return Cheque(**response)

	async def create_cheque(
		self,
		coin_id: int,
		coin_amount: int,
		password: str | None = "",
		comment: str | None = "",
	) -> Cheque:
		"""Returns created Cheque"""
		created_cheque_response = await self._make_request(
			"POST", "/user/create_cheque",
			params={
				"coin_id": coin_id,
				"coin_amount": coin_amount,
				"password": password,
				"comment": comment
			}
		)
		return await self.get_cheque(
			created_cheque_response.get("cheque_id")
		)

	async def claim_cheque(
		self,
		cheque_id: str,
		password: str | None = ""
	) -> Cheque:
		"""Returns claimed Cheque"""
		await self._make_request(
			"POST", "/user/claim_cheque",
			params={
				"cheque_id": cheque_id,
				"password": password
			}
		)
		return await self.get_cheque(cheque_id)

	async def get_my_invoices(self) -> list[Invoice]:
		"""Returns all your existing Invoices"""
		response = await self._make_request("GET", "/invoice/my_invoices")
		return [Invoice(**data) for data in response]

	async def get_invoice(self, invoice_unique_hash: str) -> Invoice:
		"""Returns Invoice"""
		response = await self._make_request("GET", "/invoice/get_invoice_data")
		return Invoice(**response)

	async def create_invoice(
		self,
		coin_id: int,
		coin_amount: int,
		expiration_time: int,
		comment: str | None = "",
		return_url: str | None = ""
	) -> Invoice:
		"""Returns created Invoice"""
		created_invoice_response = await self._make_request(
			"POST", "/invoice/create_invoice",
			params={
				"coin_id": coin_id,
				"coin_amount": coin_amount,
				"expiration_time": expiration_time,
				"comment": comment,
				"return_url": return_url
			}
		)
		return await self.get_invoice(
			created_invoice_response.get("invoice_unique_hash")
		)

	async def pay_invoice(self, invoice_unique_hash: str) -> Invoice:
		"""Returns paid Invoice"""
		await self._make_request(
			"POST", "/invoice/pay_invoice",
			params={
				"invoice_unique_hash": invoice_unique_hash
			}
		)
		return await self.get_invoice(invoice_unique_hash)

	async def delete_invoice(self, invoice_unique_hash: str) -> Invoice:
		"""Returns deleted Invoice"""
		await self._make_request(
			"POST", "/invoice/delete_invoice",
			params={
				"invoice_unique_hash": invoice_unique_hash
			}
		)
		return await self.get_invoice(invoice_unique_hash)
