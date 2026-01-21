from typing_extensions import TypedDict, NotRequired
from typing import List
class SyntaxRequest(TypedDict):
    code: str

class SyntaxResponse(TypedDict):
    result: str