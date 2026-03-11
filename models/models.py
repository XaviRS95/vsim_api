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
    correctness: bool
    coverage_report: str