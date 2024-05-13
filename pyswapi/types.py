from datetime import datetime
from dataclasses import dataclass


@dataclass
class CoinInfo:
	coin_id: int
	coin_name: str
	coin_symbol: str

	def __str__(self) -> str:
		return f"<Coin {self.coin_id}, {self.coin_name} [{self.coin_symbol}]>"

@dataclass
class Cheque:
	cheque_id: str
	is_activated: bool
	coin_id: int
	coin_amount: int
	has_password: bool
	comment: str | None

	def __str__(self) -> str:
		return f"<Cheque #{self.cheque_id}, {self.coin_id}: {self.coin_amount}>"

@dataclass
class PayHistoryItem:
	user_id: int
	pay_time: datetime
	pay_hash: str

	def __str__(self) -> str:
		return f"<PayHistoryItem #{self.pay_hash}, {self.user_id} at {self.pay_time}>"

@dataclass
class Invoice:
	invoice_unique_hash: str
	creator_id: str
	coin_id: int
	coin_amount: int
	comment: str | None
	expiration_time: int 
	creation_time: datetime
	return_url: str
	__pay_history: list[PayHistoryItem] | list

	@property
	def pay_history(self) -> list[PayHistoryItem] | list:
		return __pay_history or []

	@pay_history.setter
	def __pay_history_setter(self, value: list[PayHistoryItem] | list) -> None:
		self.pay_history = [PayHistoryItem(**data) for data in value]

	def __str__(self) -> str:
		return f"<Invoice #{self.invoice_unique_hash}, {self.creator_id}: {self.coin_amount}>"
