from fastapi.responses import JSONResponse
from fastapi import status
from models.models import SyntaxRequest, SyntaxResponse

def syntax_check(request: SyntaxRequest):




    return JSONResponse(
        content = {
            'name':API_CONFIG['name'],
            'environment': API_CONFIG['environment'],
            'version':API_CONFIG['version']},
        status_code = status.HTTP_200_OK)