from fastapi import APIRouter
from models.models import TestBenchRequest
from responses.testbench_testing_responses import testbench_testing_responses

testbench_testing_router = APIRouter()

@testbench_testing_router.post('/api/testbench_testing')
async def testbench_testing(request: TestBenchRequest):
    response = await testbench_testing_responses.testbench_testing(request = request)
    return response