from typing_extensions import TypedDict

class SyntaxRequest(TypedDict):
    code: str

class SyntaxResponse(TypedDict):
    error: bool
    error_traces: list[str]