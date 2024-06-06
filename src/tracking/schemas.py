import hashlib
from datetime import datetime
from pydantic import BaseModel, Field
from typing   import Optional


class T_Fingerprint(BaseModel):
	id         : Optional[int]
	visitor_id : int
	user_id    : Optional[int] = None
	user_agent : str
	ip         : Optional[str] = None
	hash       : Optional[str] = Field(default=None)
	created    : Optional[datetime]

	@staticmethod
	def hash_fp(user_id, user_agent, ip):
		h = hashlib.md5()
		h.update(
			f'{user_id or ""}_{user_agent}_{ip or ""}'.encode('utf-8')
		)
		return h.hexdigest

	def __pydantic_post_init__(self):
		if not self.hash:
			self.hash = self.hash_fp(self.user_id, self.user_agent, self.ip)

class T_Action(BaseModel):
	id          : int
	name        : str
	description : str
	created     : datetime

class T_Log(BaseModel):
	id             : int
	action_id      : int
	fingerprint_id : int
	created        : Optional[datetime]

class T_Item(BaseModel):
	ip         : Optional[str] = None
	hash       : Optional[str] = None
	user_id    : Optional[int] = None
	action_id  : int
	user_agent : str

	def is_hash_valid(self) -> bool:
		return self.generate_hash() == self.hash

	def generate_hash(self) -> str:
		return T_Fingerprint.hash_fp(
			self.user_id,
			self.user_agent,
			self.ip
		)

class T_Response(BaseModel):
	hash: str