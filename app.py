


import httpx
from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse, PlainTextResponse, RedirectResponse
from pydantic import BaseModel, Field, ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

import logging_  # noqa
from logging_ import logger

app = FastAPI(title="Hello, world!")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    as_validation_error = ValidationError.from_exception_data(
        str(request.url.path),
        line_errors=exc.errors(),
    )
    error_str = str(as_validation_error)
    logger.warning(error_str, exc_info=False)
    return PlainTextResponse(error_str, status_code=422)


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.warning(exc, exc_info=exc)
    return await http_exception_handler(request, exc)


@app.get("/")
async def redirect_to_docs():
    return RedirectResponse(url="/docs")


@app.get("/clickable-log")
async def clickable_log():
    from logging_ import logger

    logger.info("This will show with source code location and timing")
    return JSONResponse({"message": "Clickable log!"})


@app.get("/error")
async def error():
    raise Exception("This is a test error")


class SomeData(BaseModel):
    a: int = Field(..., ge=10)


@app.post("/error-validation-error")
async def error_validation_error(data: SomeData):
    return True


@app.get("/error-httpx-timeout")
async def error_httpx():
    httpx.get("http://12312312", timeout=1)


@app.get("/error-httpx-connection-refused")
async def error_httpx_connection_refused():
    httpx.get("http://localhost:11111", timeout=1)


@app.get("/error-404")
async def error_404():
    raise HTTPException(status_code=404, detail="Not Found")
