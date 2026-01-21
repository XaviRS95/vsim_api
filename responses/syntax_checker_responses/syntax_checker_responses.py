from fastapi.responses import JSONResponse
from fastapi import status
from models.models import SyntaxResponse
from utils.vsim_utils import syntax_checker

async def syntax_check(code:str)-> SyntaxResponse:
    response = syntax_checker(code=code)
    return response
