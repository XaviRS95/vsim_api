from models.models import TestBenchRequest, TestBenchResponse
from utils.vsim_utils import testbench_checker

async def testbench_testing(request: TestBenchRequest)-> TestBenchResponse:
    response = testbench_checker(request=request)
    return response