#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-10-14 19:42
# Author:  rongli
# Email:   abc@xyz.com
# File:    router_class.py
# Project: fa-demo
# IDE:     PyCharm
import gzip
import time
from enum import Enum
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Sequence,
    Type,
    Union,
)

from fastapi import HTTPException, params, Request, Response
from fastapi.datastructures import Default
from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRoute, APIRouter
from fastapi.utils import (
    generate_unique_id,
)
from loguru import logger
from starlette import routing
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse
from starlette.routing import BaseRoute, Mount as Mount  # noqa
from starlette.types import ASGIApp


class GzipRequest(Request):
    async def body(self) -> bytes:
        if not hasattr(self, "_body"):
            body = await super().body()
            if "gzip" in self.headers.getlist("Content-Encoding"):
                body = gzip.decompress(body)
            self._body = body  # noqa
        return self._body


class GzipRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request = GzipRequest(request.scope, request.receive)
            return await original_route_handler(request)

        return custom_route_handler


class ValidationErrorLoggingRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except RequestValidationError as exc:
                body = await request.body()
                detail = {"errors": exc.errors(), "body": body.decode()}
                raise HTTPException(status_code=422, detail=detail)

        return custom_route_handler


class TimedRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            before = time.time()
            response: Response = await original_route_handler(request)
            duration = time.time() - before
            response.headers["X-Response-Time"] = str(duration)
            # print(f"route duration: {duration}")
            # print(f"route response: {response}")
            # print(f"route response headers: {response.headers}")
            return response

        return custom_route_handler


class LoggingRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            logger.debug(f'start  {request.url}')
            logger.debug(f"request  body: {await request.body()}")
            response: Response = await original_route_handler(request)
            logger.debug(f"response body: {response.body}")
            logger.debug(f'end    {request.url}')
            return response

        return custom_route_handler


class LoggingAPIRouter(APIRouter):
    def __init__(
            self,
            *,
            prefix: str = "",
            tags: Optional[List[Union[str, Enum]]] = None,
            dependencies: Optional[Sequence[params.Depends]] = None,
            default_response_class: Type[Response] = Default(JSONResponse),
            responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
            callbacks: Optional[List[BaseRoute]] = None,
            routes: Optional[List[routing.BaseRoute]] = None,
            redirect_slashes: bool = True,
            default: Optional[ASGIApp] = None,
            dependency_overrides_provider: Optional[Any] = None,
            route_class: Type[APIRoute] = APIRoute,
            on_startup: Optional[Sequence[Callable[[], Any]]] = None,
            on_shutdown: Optional[Sequence[Callable[[], Any]]] = None,
            deprecated: Optional[bool] = None,
            include_in_schema: bool = True,
            generate_unique_id_function: Callable[[APIRoute], str] = Default(
                    generate_unique_id
            ),
    ) -> None:
        super().__init__(
                prefix=prefix,
                tags=tags,
                dependencies=dependencies,
                default_response_class=default_response_class,
                responses=responses,
                callbacks=callbacks,
                routes=routes,
                redirect_slashes=redirect_slashes,
                default=default,
                dependency_overrides_provider=dependency_overrides_provider,
                route_class=route_class,
                on_startup=on_startup,
                on_shutdown=on_shutdown,
                deprecated=deprecated,
                include_in_schema=include_in_schema,
                generate_unique_id_function=generate_unique_id_function,
        )

        self.route_class = LoggingRoute
