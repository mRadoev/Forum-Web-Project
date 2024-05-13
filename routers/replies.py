from fastapi import APIRouter, Query, Response, Header
from services import topics_services, reply_services, users_service
from common import responses
from data.models import Topic, Reply, Vote
from fastapi.responses import JSONResponse
from common.auth import get_user_or_raise_401


replies_router = APIRouter(prefix='/replies')


@replies_router.post('/vote/{reply_id}')
def give_vote(vote: Vote, reply_id: int,  x_token: str = Header()):
    get_user_or_raise_401(x_token)
    data = users_service.decode_token(x_token)
    if reply_services.check_id_existence(reply_id):
        return JSONResponse(status_code=404, content={'detail': 'Reply with this id was not found'})

    if reply_services.check_reply_vote_existence(data.get("id"), reply_id):
        return responses.BadRequest("You already voted to that reply!")

    return reply_services.vote_to_reply(vote, reply_id, data.get("id"))


@replies_router.put('/vote/{reply_id}')
def update_vote(vote: Vote, reply_id: int,  x_token: str = Header()):
    get_user_or_raise_401(x_token)
    data = users_service.decode_token(x_token)
    if reply_services.check_id_existence(reply_id):
        return JSONResponse(status_code=404, content={'detail': 'Reply with this id was not found'})

    update = reply_services.update_vote(vote, reply_id, data.get("id"))
    if update is None:
        return responses.BadRequest("Check info you've given, or check if you have voted on this particular reply")

    if update == 1:
        return "You successfully updated your vote."

@replies_router.get('/{reply_id}')
def reply_info(reply_id: int):
    if reply_services.check_id_existence(reply_id):
        return JSONResponse(status_code=404, content={'detail': 'Reply with this id was not found'})

    return reply_services.get_reply_info(reply_id)

