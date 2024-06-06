from src.tracking         import service  
from src.tracking.schemas import T_Item


async def track_action(item: T_Item) -> str:
	if action := await service.get_action_by_id(item.action_id):

		fp = None
		if item.hash:
			if item.is_hash_valid():
				fp = await service.get_fp_by_hash(item.hash)
			else:
				fp         = await service.get_fp_by_hash(item.generate_hash())
				visitor_id = fp.visitor_id if fp else None

				fp = await service.create_fp({
					'ip'         : item.ip,
					'user_id'    : item.user_id,
					'user_agent' : item.user_agent,
					'visitor_id' : visitor_id
				})
		else:
			fp         = await service.get_fp_by_hash(item.generate_hash())
			visitor_id = fp.visitor_id if fp else None
			
			fp = await service.create_fp({
				'ip'         : item.ip,
				'user_id'    : item.user_id,
				'user_agent' : item.user_agent,
				'visitor_id' : visitor_id
			})

		service.create_t_log({
			'action_id'      : action.id,
			'fingerprint_id' : fp.id
		})

		return fp.hash
	return ''

