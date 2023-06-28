import uuid
from typing import Any, Dict, Union

from fastapi import Request

from app.utils import static


async def is_initial(data: Dict[Any, Any], request: Request) -> bool:
    author = static.get_author(data)

    if await request.app.mongodb["data"].find_one({"author": author}):
        return False
    return True


async def is_user_interested_field(data: Dict[Any, Any], request: Request) -> bool:
    author = static.get_author(data)
    user = await request.app.mongodb["data"].find_one({"author": author})
    return "interested" in user


async def is_user_interested(data: Dict[Any, Any], request: Request) -> bool:
    author = static.get_author(data)
    user = await request.app.mongodb["data"].find_one({"author": author})
    return user["interested"]


async def is_username_field(data: Dict[Any, Any], request: Request) -> bool:
    author = static.get_author(data)
    user = await request.app.mongodb["data"].find_one({"author": author})
    return "username" in user


async def is_email_field(data: Dict[Any, Any], request: Request) -> bool:
    author = static.get_author(data)
    user = await request.app.mongodb["data"].find_one({"author": author})
    return "email" in user


async def is_experience_field(data: Dict[Any, Any], request: Request) -> bool:
    author = static.get_author(data)
    user = await request.app.mongodb["data"].find_one({"author": author})
    return "experience" in user


async def add_user(data: Dict[Any, Any], request: Request) -> bool:
    author = static.get_author(data)
    author_id = static.get_author_id(data)
    user = {
        "_id": uuid.uuid4().hex,
        "author": author,
        "author_id": author_id,
    }
    try:
        await request.app.mongodb["data"].insert_one(user)
        return True
    except Exception as e:
        print(e)
        return False


async def add_user_interested(
    data: Dict[Any, Any], request: Request, interested: bool
) -> bool:
    author = static.get_author(data)
    try:
        await request.app.mongodb["data"].update_one(
            {"author": author},
            {"$set": {"interested": interested}},
        )
        return True
    except Exception as e:
        print(e)
        return False


async def add_username(data: Dict[Any, Any], request: Request, username: str) -> bool:
    author = static.get_author(data)
    try:
        await request.app.mongodb["data"].update_one(
            {"author": author},
            {"$set": {"username": username}},
        )
        return True
    except Exception as e:
        print(e)
        return False


async def add_email(data: Dict[Any, Any], request: Request, email: str) -> bool:
    author = static.get_author(data)
    try:
        await request.app.mongodb["data"].update_one(
            {"author": author},
            {"$set": {"email": email}},
        )
        return True
    except Exception as e:
        print(e)
        return False


async def add_experience(
    data: Dict[Any, Any], request: Request, experience: Union[int, str]
) -> bool:
    author = static.get_author(data)
    try:
        await request.app.mongodb["data"].update_one(
            {"author": author},
            {"$set": {"experience": experience}},
        )
        return True
    except Exception as e:
        print(e)
        return False
