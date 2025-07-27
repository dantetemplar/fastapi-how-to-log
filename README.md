# FastAPI Enhanced Logging

A comprehensive logging solution for FastAPI applications that provides enhanced debugging capabilities, performance monitoring, and cleaner log output.

## Features

### 🔗 Clickable Source Code Links
- **IDE Integration**: Log messages include clickable file paths that work in both PyCharm and VS Code
- **Precise Location**: Shows exact line numbers where log messages originate
- **Relative Paths**: Uses relative paths for cleaner output

https://github.com/user-attachments/assets/1badb8a6-b525-405e-8e5f-e5585be2be37

### 🧹 Clean Log Output
- **Reduced Boilerplate**: Filters out verbose FastAPI and uvicorn logs
- **HTTPX Filtering**: Suppresses noisy HTTP client library logs
- **Error Focus**: Shows only your application's errors, not framework noise
- **Stack Trace Cleanup**: Removes irrelevant framework stack


https://github.com/user-attachments/assets/572d0217-c10d-4af8-b4d8-deeac88ceb54

### ⏱️ Performance Monitoring
- **Handler Timing**: Automatically measures and logs execution time for each endpoint handler

<img width="864" height="280" alt="image" src="https://github.com/user-attachments/assets/b8f3dbb0-77b8-4fcd-92cb-5bab1395f6c8" />

### 🚨 Exception Handling & Logging
- **Validation Error Logging**: Automatically logs Pydantic validation errors with detailed context
- **HTTP Exception Tracking**: Captures and logs HTTP exceptions with proper error details
- **Human Readable Error Messages**: Returns clean error messages while maintaining comprehensive logging

<img width="916" height="378" alt="image" src="https://github.com/user-attachments/assets/e26e14e6-935e-4026-8a35-7dfe5d7fa25c" />


## Usage

Copy the `logging_.py` module into your project and use it as follows:

```python
import logging_  # noqa
from logging_ import logger

from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import PlainTextResponse
from pydantic import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

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
async def root():
    logger.info("This will show with source code location and timing")
    return {"message": "Hello World"}

@app.get("/error")
async def error():
    raise Exception("This is a test error")
```

## Example Output

```
[2025-07-27 20:24:48,880] [INFO] [File "app.py", line 19] This will show with source code location and timing
[2025-07-27 20:24:48,880] [INFO] [File "app.py", line 20] Handler `root` took 1 ms

```

The file path in the log message will be clickable ([File "app.py", line 19]) in your IDE, taking you directly to the source code.

## Configuration

The logging configuration is automatically set up with:

- **Source Code Logger**: `src` logger with file path and line number information
- **Access Logs**: Clean uvicorn access logs
- **Error Logs**: Filtered error logs with cleaned stack traces
- **HTTPX Suppression**: Reduces HTTP client library noise

## Customization

You can modify the `dictConfig` in `logging_.py` to adjust:

- Log levels for different components
- Output formatting
- Color schemes
- Filtered paths and libraries

## How It Works

### Source Code Linking
The `RelativePathFilter` adds relative file paths to log records, making them clickable in IDEs.

### Performance Monitoring
The `run_endpoint_function` is monkey-patched into FastAPI to automatically measure handler execution time.

### Log Filtering
The `CleanErrorFilter` removes framework noise from stack traces and suppresses unwanted log sources.

### Exception Handling
The custom exception handlers provide structured logging for validation errors and HTTP exceptions:

- **Validation Errors**: Converts FastAPI's `RequestValidationError` to Pydantic's `ValidationError` format for human readable messages
- **HTTP Exceptions**: Logs HTTP exceptions with full context while maintaining FastAPI's default error response behavior

## ⚠️ Disclaimer

**This solution uses some "cursed" techniques:**

- **Monkey Patching**: Directly modifies FastAPI's internal `run_endpoint_function`
- **Internal API Usage**: Relies on FastAPI's internal dependency injection system
- **Framework Coupling**: Tightly coupled to specific FastAPI and Starlette versions

While effective, these techniques may break with framework updates. Use at your own risk in production environments.

## Requirements

- Python 3.11+
- FastAPI
- colorlog
- uvicorn (for ASGI server)

## License

MIT License - feel free to use and modify as needed.
