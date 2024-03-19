import json
import time
from fastapi import Request
from starlette.concurrency import iterate_in_threadpool

from app.core import logger


async def logging_middleware(request: Request, call_next):
    start = time.time()

    # extract data
    headers = {key: value for key, value in request.headers.items() if key.lower() in ['content-type', 'authorization']}
    request_body = await request.body()

    # write log for request
    request_log_dict = {
        'type': 'request',
        'url': request.url.path,
        'method': request.method,
        'headers': headers,
        'cookies': request.cookies,
        'body': json.loads(request_body) if request_body else None
    }
    logger.info(request_log_dict)

    # call next
    response = await call_next(request)

    response_body = [section async for section in response.body_iterator]
    response.body_iterator = iterate_in_threadpool(iter(response_body))
    try:
        response_body = json.loads(response_body[0].decode())
    except Exception as e:
        response_body = None

    process_time = time.time() - start

    # write log for response
    response_log_dict = {
        'type': 'response',
        'process_time': process_time
    }

    if response_body:
        response_log_dict['status_code'] = response_body.get('status_code')
        response_log_dict['detail'] = response_body.get('detail')
        response_log_dict['result'] = response_body.get('result')

    logger.info(response_log_dict)

    return response
