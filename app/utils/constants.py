import os

from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
BASE_URI = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}"

HEADERS = {
    "Content-Type": "application/json",
}

INTERACTIVE_BOILERPLATE = {
    "messaging_product": "whatsapp",
    "recipient_type": "individual",
    "to": "",
    "type": "interactive",
    "interactive": {
        "type": "",
        "header": {},
        "body": {
            "text": "",
        },
        "footer": {
            "text": "",
        },
        "action": {},
    },
}

EXP_DICT = {
    "exp-1": 1,
    "exp-2": 2,
    "exp-3": 3,
    "exp-4": 4,
    "exp-5": 5,
}

INITIAL_MESSAGE_DICT = {
    "header": {
        "type": "text",
        "text": "Welcome to NotBot!",
    },
    "content": "Hi! Are you here to apply for the Internship?",
    "end_text": "Please select an option below.",
    "buttons": [
        {"type": "reply", "reply": {"id": "s1-yes", "title": "Yes"}},
        {"type": "reply", "reply": {"id": "s1-no", "title": "No"}},
    ],
}

EXPERIENCE_LIST_DICT = {
    "header": {
        "type": "text",
        "text": "Experience",
    },
    "content": "Please select how many years of experience you have with Python/JS/Automation Development.",
    "end_text": "Please select an option from the list below.",
    "button_content": "Select",
    "sections": [
        {
            "title": "Years of Experience",
            "rows": [
                {
                    "id": "exp-1",
                    "title": "1 Year",
                },
                {
                    "id": "exp-2",
                    "title": "2 Years",
                },
                {
                    "id": "exp-3",
                    "title": "3 Years",
                },
                {
                    "id": "exp-4",
                    "title": "4 Years",
                },
                {
                    "id": "exp-5",
                    "title": "5 Years",
                },
            ],
        }
    ],
}
