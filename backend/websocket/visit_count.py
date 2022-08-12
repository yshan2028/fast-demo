#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-08-12 18:34
# Author:  rongli
# Email:   abc@xyz.com
# File:    visit_count.py
# Project: fa-demo
# IDE:     PyCharm
import asyncio
import datetime
import random

from fastapi import APIRouter, Path, WebSocket, WebSocketDisconnect
from starlette import status
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK

from ..dependencies import check_user_status, get_user_or_none_by_token

router = APIRouter()


@router.websocket("/{token}")
async def websocket_endpoint(websocket: WebSocket, token: str = Path(...)):
    user = await get_user_or_none_by_token(token)
    if user is None or not check_user_status(user):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    await websocket.accept()
    try:
        while True:
            time_str = datetime.datetime.now().strftime("%H:%M:%S")
            await websocket.send_json({"time": time_str, "count": random.randint(51, 100)})
            await asyncio.sleep(2)
    except (WebSocketDisconnect, ConnectionClosedOK, ConnectionClosedError):
        pass
