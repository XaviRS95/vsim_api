from config.config import API_CONFIG
from fastapi import FastAPI
from routers.syntax_checker_routers.syntax_checker_routers import syntax_checker_router
from routers.testbench_testing_routers.testbench_testing_routers import testbench_testing_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title=API_CONFIG['name'])

app.include_router(syntax_checker_router)
app.include_router(testbench_testing_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=API_CONFIG['middleware_allow_origins'],
    allow_credentials=True,
    allow_methods=API_CONFIG['middleware_allow_methods'],
    allow_headers=API_CONFIG['middleware_allow_headers'],
)