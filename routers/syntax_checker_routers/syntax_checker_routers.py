from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from config.config import API_CONFIG

syntax_checker_router = APIRouter()

@syntax_checker_router.get('/api/syntax_checker')
async def syntax_checker(request: SyntaxRequest):
    response = ""
    return response