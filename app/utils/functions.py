import json
from typing import Any, Dict, List, Optional

import requests

from app.utils import static
from app.utils.constants import ACCESS_TOKEN, BASE_URI, HEADERS, INTERACTIVE_BOILERPLATE


def send(
    data: Dict[Any, Any], content: str = " ", preview_url: bool = True
) -> Dict[Any, Any]:
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": static.get_author(data),
        "type": "text",
        "text": {"body": content, "preview_url": preview_url},
    }

    response = requests.post(
        f"{BASE_URI}/messages?access_token={ACCESS_TOKEN}",
        data=json.dumps(data),
        headers=HEADERS,
    )
    return response.json()


def send_button(
    data: Dict[Any, Any],
    header: Optional[Dict[Any, Any]],
    content: str,
    end_text: Optional[str],
    buttons: List[Dict[Any, Any]],
) -> Dict[Any, Any]:
    interactive = INTERACTIVE_BOILERPLATE.copy()
    interactive["interactive"]["type"] = "button"
    interactive["interactive"]["body"]["text"] = content
    interactive["interactive"]["action"]["buttons"] = buttons

    if header:
        interactive["interactive"]["header"] = header

    if end_text:
        interactive["interactive"]["footer"]["text"] = end_text

    interactive["to"] = static.get_author(data)

    response = requests.post(
        f"{BASE_URI}/messages?access_token={ACCESS_TOKEN}",
        data=json.dumps(interactive),
        headers=HEADERS,
    )
    return response.json()


def send_list(
    data: Dict[Any, Any],
    header: Optional[Dict[Any, Any]],
    content: str,
    end_text: Optional[str],
    button_content: str,
    sections: List[Dict[Any, Any]],
) -> Dict[Any, Any]:
    interactive = INTERACTIVE_BOILERPLATE.copy()
    interactive["interactive"]["type"] = "list"
    interactive["interactive"]["body"]["text"] = content
    interactive["interactive"]["action"]["button"] = button_content
    interactive["interactive"]["action"]["sections"] = sections

    if header:
        interactive["interactive"]["header"] = header

    if end_text:
        interactive["interactive"]["footer"]["text"] = end_text

    interactive["to"] = static.get_author(data)

    response = requests.post(
        f"{BASE_URI}/messages?access_token={ACCESS_TOKEN}",
        data=json.dumps(interactive),
        headers=HEADERS,
    )
    return response.json()
