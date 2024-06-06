from fastapi import APIRouter, status

from src.tracking.schemas import T_Request, T_Response
from src.tracking         import usecases

router = APIRouter()


@router.post('/track', status_code=status.HTTP_200_OK, response_model=T_Response)
async def track(request: T_Request) -> T_Response:
	hash_str = await usecases.track_action(request)
	return T_Response(hash=hash_str)
