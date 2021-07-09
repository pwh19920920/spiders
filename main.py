import importlib
import json
import os
import re

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from api.base import BaseResponseModel

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    data = BaseResponseModel(ok=False, msg="数据格式不符合要求")
    return JSONResponse(data.__dict__, status_code=400)


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    data = BaseResponseModel(ok=False, msg="系统开小差")
    return JSONResponse(data.__dict__, status_code=500)


@app.get('/')
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


def register_api(app: FastAPI):
    module_names = []
    for file in os.listdir('api'):
        if file in ('__pycache__', 'base.py', '__init__.py'):
            continue
        # .py
        if module_name := re.findall(r'(\w+)\.py', file):
            module_names.append(module_name[0])
        else:
            # package
            module_names.append(file)

    for module_name in module_names:
        module = importlib.import_module(f'api.{module_name}')
        if hasattr(module, 'ResponseModel') and hasattr(module, 'process'):
            app.post(
                f'/{module_name}',
                response_model=module.ResponseModel,
                description=module.__doc__ or '',
            )(module.process)


register_api(app)
