from src.tracking         import service  
from src.tracking.schemas import T_Request


async def track_action(req: T_Request) -> str:
	if action := await service.get_action_by_id(req.action_id):

		fp = None
		if req.hash:
			if req.is_hash_valid():
				fp = await service.get_fp_by_hash(req.hash)
			else:
				fp         = await service.get_fp_by_hash(req.generate_hash())
				visitor_id = fp.visitor_id if fp else None

				fp = await service.create_fp({
					'ip'         : req.ip,
					'user_id'    : req.user_id,
					'user_agent' : req.user_agent,
					'visitor_id' : visitor_id
				})
		else:
			fp         = await service.get_fp_by_hash(req.generate_hash())
			visitor_id = fp.visitor_id if fp else None
			fp = await service.create_fp({
				'ip'         : req.ip,
				'user_id'    : req.user_id,
				'user_agent' : req.user_agent,
				'visitor_id' : visitor_id
			})

		await service.create_t_log({
			'action_id'      : action.id,
			'fingerprint_id' : fp.id
		})

		return fp.hash
	return ''

