import json
from typing import Any, Dict

from fastapi import APIRouter, Query, Request
from fastapi.responses import JSONResponse

import app.crud as crud
from app.utils import functions, static
from app.utils.constants import (
    ACCESS_TOKEN,
    EXP_DICT,
    EXPERIENCE_LIST_DICT,
    INITIAL_MESSAGE_DICT,
)

router = APIRouter(
    prefix="/whatsapp",
    tags=["whatsapp"],
    responses={404: {"description": "Not found"}},
)


def send_message(body: Dict[Any, Any], message: str) -> Dict[Any, Any]:
    resp = functions.send(
        data=body,
        content=message,
    )
    return resp


def send_initial_message(body: Dict[Any, Any]) -> Dict[Any, Any]:
    resp = functions.send_button(
        body,
        header=INITIAL_MESSAGE_DICT["header"],
        content=INITIAL_MESSAGE_DICT["content"],
        end_text=INITIAL_MESSAGE_DICT["end_text"],
        buttons=INITIAL_MESSAGE_DICT["buttons"],
    )
    return resp


def send_experience_list(body: Dict[Any, Any]) -> Dict[Any, Any]:
    resp = functions.send_list(
        body,
        header=EXPERIENCE_LIST_DICT["header"],
        content=EXPERIENCE_LIST_DICT["content"],
        end_text=EXPERIENCE_LIST_DICT["end_text"],
        button_content=EXPERIENCE_LIST_DICT["button_content"],
        sections=EXPERIENCE_LIST_DICT["sections"],
    )
    return resp


@router.post("/webhook")
async def message(request: Request):
    body = await request.json()

    if static.is_message(body):
        if static.is_interactive_button_reply(body):
            return await handle_interactive_button_reply(body, request)
        elif static.is_interactive_list_reply(body):
            return await handle_interactive_list_reply(body, request)

        return await handle_other_message(body, request)

    print("Not a message/interactivity")
    return JSONResponse(status_code=200, content="Not a message")


async def handle_interactive_button_reply(body: Dict[Any, Any], request: Request):
    if not await crud.is_user_interested_field(body, request):
        user_resp = static.get_interactive_reply(body)

        if user_resp["button_reply"]["id"] == "s1-yes":
            user_interested = await crud.add_user_interested(body, request, True)
            if user_interested:
                name_msg = send_message(body, "Please enter your name")
                return JSONResponse(status_code=200, content=name_msg)
            print("[ERROR] User interested not added")

        elif user_resp["button_reply"]["id"] == "s1-no":
            user_interested = await crud.add_user_interested(body, request, False)
            if user_interested:
                goodbye_msg = send_message(body, "Thank you for your time. Goodbye!")
                return JSONResponse(status_code=200, content=goodbye_msg)
            print("[ERROR] User interested not added")

        err_msg = send_message(
            body, "Sorry, I didn't understand that. Please try again."
        )
        return JSONResponse(status_code=200, content=err_msg)

    print("[ERROR] Invalid interactive button reply")
    return JSONResponse(status_code=200, content="Invalid interactive button reply")


async def handle_interactive_list_reply(body: Dict[Any, Any], request: Request):
    if await crud.is_email_field(body, request) and not await crud.is_experience_field(
        body, request
    ):
        user_resp = static.get_interactive_reply(body)["list_reply"]["id"]
        user_exp = EXP_DICT.get(user_resp)
        if user_exp:
            add_experience = await crud.add_experience(body, request, user_exp)
            if add_experience:
                goodbye_msg = send_message(body, "Thank you for your time. Goodbye!")
                return JSONResponse(status_code=200, content=goodbye_msg)
            print("[ERROR] Experience not added")

    print("[ERROR] Invalid interactive list reply")
    return JSONResponse(status_code=200, content="Invalid interactive list reply")


async def handle_other_message(body: Dict[Any, Any], request: Request):
    if await crud.is_initial(body, request):
        add_user = await crud.add_user(body, request)
        if add_user:
            resp = send_initial_message(body)
            return JSONResponse(status_code=200, content=resp)
        print("[ERROR] User not added")
    elif await crud.is_user_interested(
        body, request
    ) and not await crud.is_username_field(body, request):
        user_resp = static.get_message(body)
        if static.is_username(user_resp):
            add_username = await crud.add_username(body, request, user_resp)
            if add_username:
                email_msg = send_message(body, "Please enter your email")
                return JSONResponse(status_code=200, content=email_msg)
            print("[ERROR] Username not added")

        err_msg = send_message(
            body, "Sorry, I didn't understand that. Please try again."
        )
        return JSONResponse(status_code=200, content=err_msg)

    elif await crud.is_username_field(body, request) and not await crud.is_email_field(
        body, request
    ):
        user_resp = static.get_message(body)
        if static.is_email(user_resp):
            add_email = await crud.add_email(body, request, user_resp)
            if add_email:
                exp_msg = send_experience_list(body)
                return JSONResponse(status_code=200, content=exp_msg)
            print("[ERROR] Email not added")

        err_msg = send_message(
            body, "Sorry, I didn't understand that. Please try again."
        )
        return JSONResponse(status_code=200, content=err_msg)

    print("[Log] Not a valid message. Probably due to completed form.")
    return JSONResponse(status_code=200, content="Not a valid message")


@router.get("/webhook")
async def verify_token(
    hub_mode: str = Query(..., alias="hub.mode"),
    hub_challenge: int = Query(..., alias="hub.challenge"),
    hub_verify_token: str = Query(..., alias="hub.verify_token"),
):
    if hub_mode == "subscribe" and hub_verify_token == ACCESS_TOKEN:
        return JSONResponse(status_code=200, content=int(hub_challenge))
    return JSONResponse(status_code=403, content="Forbidden")
