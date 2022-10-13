#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-10-13 13:53
# Author:  rongli
# Email:   abc@xyz.com
# File:    oauth_login.py
# Project: fa-demo
# IDE:     PyCharm

from fastapi import APIRouter, Depends, Form, Query
from starlette.requests import Request
from starlette.responses import HTMLResponse

from ..config import settings
from ..dependencies import get_current_active_user
from ..models import User

router = APIRouter(prefix='/oauth')


@router.get('/authorize', summary='授权', response_class=HTMLResponse)
async def authorize(request: Request,
                    response_type: str = Query("code"),
                    client_id: str = Query(...),
                    redirect_uri: str = Query(...),
                    scope: str = Query(...),
                    state: str = Query(...),
                    ):

    # 这里面可以用client_id去数据库里面查询 app_name
    app_name = "notebook站点"

    context = {'request': request, "app_name": app_name,
               "response_type": response_type, "login_url": settings.swagger_ui_oauth2_redirect_url,
               "client_id": client_id, "redirect_uri": redirect_uri,
               "scope": scope, "state": state,
               }
    code = "AUTHORIZATION_CODE"
    # return RedirectResponse(f"{redirect_uri}?code={code}&state={state}")
    return request.app.state.jinja.TemplateResponse("oauth/authorize.html", context=context)


@router.post('/code', summary='授权码', )
async def authorize(request: Request,
                    response_type: str = Query("code"),
                    client_id: str = Query(...),
                    redirect_uri: str = Query(...),
                    scope: str = Query(...),
                    state: str = Query(...),
                    me: User = Depends(get_current_active_user)
                    ):
    if response_type != 'code':
        return {"response_type": response_type}
    # 这里 要保存 userid username 到 redis   {code: username}
    # 此处应该去数据库中查询相应的 client_id 这些信息是否正确
    # 并且要确定用的是同一个state
    code = "uuid.uuid4().hex"  # 下发 授权码
    return {"code": code, "state": state, "redirect_uri": redirect_uri}


@router.post('/token', summary='token')
async def get_token(client_id: str = Form(...),
                    client_secret: str = Form(...),
                    grant_type: str = Form('authorization_code'),
                    code: str = Form(...),
                    redirect_uri: str = Form(...),
                    ):
    # 要检验 client_id 和 client_secret, code
    # 用前面生成的 userid 生成 token
    # 去 redis 取 userid, username
    # username = 'admin'
    # access_token = create_access_token(data={"sub": username})
    # token = Token(access_token=access_token, token_type='bearer')
    # data = token.dict(by_alias=False)
    # return data
    print(client_id, client_secret, grant_type, code, redirect_uri)
    access_token = "access_token"
    return {"access_token": access_token, "token_type": "bearer"}


@router.get('/profile', summary='用户信息', )
async def profile(me: User = Depends(get_current_active_user)):
    return me
