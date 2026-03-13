from typing_extensions import TypedDict

class SyntaxRequest(TypedDict):
    code: str

class SyntaxResponse(TypedDict):
    result: str

class TestBenchRequest(TypedDict):
    testbench: str
    dut: str
    asserts: str

class TestBenchResponse(TypedDict):
    total_errors: int
    coverage_pct: float
    testing_data: str