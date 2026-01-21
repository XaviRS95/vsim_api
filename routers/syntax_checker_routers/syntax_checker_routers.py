from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from config.config import API_CONFIG
from models.models import SyntaxRequest
from responses.syntax_checker_responses import syntax_checker_responses

syntax_checker_router = APIRouter()

@syntax_checker_router.post('/api/syntax_checker')
async def syntax_checker(request: SyntaxRequest):
    response = await syntax_checker_responses.syntax_check(code=request['code'])
    return response