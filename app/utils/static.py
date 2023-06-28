from typing import Any, Dict

import regex as re


@staticmethod
def is_message(data: Dict[Any, Any]) -> bool:
    data = data["entry"][0]["changes"][0]["value"]
    if "messages" in data:
        return True
    return False


@staticmethod
def is_username(username: str) -> bool:
    if re.match(r"^[a-zA-Z ]+$", username):
        return True
    return False


@staticmethod
def is_email(email: str) -> bool:
    if re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
        return True
    return False


@staticmethod
def get_message(data: Dict[Any, Any]) -> str | None:
    data = data["entry"][0]["changes"][0]["value"]
    if "messages" in data:
        return data["messages"][0]["text"]["body"]
    return None


@staticmethod
def get_author(data: Dict[Any, Any]) -> str | None:
    try:
        return data["entry"][0]["changes"][0]["value"]["messages"][0]["from"]
    except Exception:
        return None


@staticmethod
def get_author_id(data: Dict[Any, Any]) -> str | None:
    try:
        return data["entry"][0]["changes"][0]["value"]["metadata"]["phone_number_id"]
    except Exception:
        return None


@staticmethod
def is_interactive_button_reply(data: Dict[Any, Any]) -> bool:
    try:
        if (
            data["entry"][0]["changes"][0]["value"]["messages"][0]["interactive"][
                "type"
            ]
            == "button_reply"
        ):
            return True
        return False
    except Exception:
        return False


@staticmethod
def is_interactive_list_reply(data: Dict[Any, Any]) -> bool:
    try:
        if (
            data["entry"][0]["changes"][0]["value"]["messages"][0]["interactive"][
                "type"
            ]
            == "list_reply"
        ):
            return True
        return False
    except Exception:
        return False


@staticmethod
def get_interactive_reply(data: Dict[Any, Any]) -> str | None:
    try:
        return data["entry"][0]["changes"][0]["value"]["messages"][0]["interactive"]
    except Exception:
        return None
