
from sqlalchemy import insert, select, func

from src.database         import fetch_one, execute
from src.models           import t_fingerprint, t_action, t_log
from src.tracking.schemas import T_Fingerprint, T_Action


################ T_Fingerprint ################

async def create_fp(fp_data: dict) -> T_Fingerprint:
	if not fp_data.get('visitor_id'):
		last_visitor_id = await get_last_fp_visitor_id()
		fp_data['visitor_id'] = last_visitor_id + 1 if last_visitor_id is not None else 0

	fp  = T_Fingerprint(**fp_data)
	row = await fetch_one(
		insert(t_fingerprint)
		.values(fp.model_dump())
		.returning(t_fingerprint)
	)
	
	return T_Fingerprint(**row)


async def get_fp_by_hash(hash: str) -> T_Fingerprint | None:
	row = await fetch_one(
		select(t_fingerprint)
		.where(t_fingerprint.c.hash == hash)
	)
	if row:
		return T_Fingerprint(**row)


async def get_last_fp_visitor_id() -> int | None:
	row = await fetch_one(
		select(t_fingerprint)
		.where(
			t_fingerprint.c.visitor_id == select(func.max(t_fingerprint.c.visitor_id))
		)
	)
	if row:
		return int(row['visitor_id'])

################ T_Action ################

async def get_action_by_id(id: int) -> T_Action | None:
	row = await fetch_one(
		select(t_action)
		.where(t_action.c.id == id)
	)

	if row:
		return T_Action(**row)

################ T_Log ################

async def create_t_log(t_log_data: dict):
	await execute(
		insert(t_log).
		vaues(t_log_data)
	)