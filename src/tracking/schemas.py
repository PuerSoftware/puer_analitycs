import hashlib

from datetime import datetime
from pydantic import BaseModel
from typing   import Optional


############### T_Fingerprint ###############

class BaseT_Fingerprint(BaseModel):
	visitor_id : int
	user_id    : Optional[int] = None
	user_agent : str
	ip         : Optional[str] = None
	hash       : str

	@staticmethod
	def hash_fp(user_id, user_agent, ip):
		h = hashlib.md5()
		h.update(
			f'{user_id or ""}_{user_agent}_{ip or ""}'.encode('utf-8')
		)
		return h.hexdigest()

	def __init__(self, **data):
		if data.get('hash') is None:
			data['hash'] = self.hash_fp(
				data.get('user_id'),
				data['user_agent'],
				data.get('ip')
			)
		super().__init__(**data)


class T_FingerprintCreate(BaseT_Fingerprint):
	...


class T_Fingerprint(BaseT_Fingerprint):
	id         : int
	created    : datetime


############### T_Action ###############

class T_Action(BaseModel):
	id          : int
	name        : str
	description : str
	created     : datetime

############### T_Log ###############

class T_Log(BaseModel):
	id             : int
	action_id      : int
	fingerprint_id : int
	created        : Optional[datetime]


############### REQUEST / RESPONSE ###############

class T_Request(BaseModel):
	ip         : Optional[str] = None
	hash       : Optional[str] = None
	user_id    : Optional[int] = None
	action_id  : int
	user_agent : str

	def is_hash_valid(self) -> bool:
		return self.generate_hash() == self.hash

	def generate_hash(self) -> str:
		return BaseT_Fingerprint.hash_fp(
			self.user_id,
			self.user_agent,
			self.ip
		)


class T_Response(BaseModel):
	hash: str