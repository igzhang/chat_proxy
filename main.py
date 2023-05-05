import os
import traceback
import time
import openai
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel


openai.proxy = os.getenv('proxy')
app = FastAPI()

messages = []
messages_update_timestamp = 0
messages_cache_time = 3600


class Item(BaseModel):
    content: str


def clear_messages_session(update_time: float, now: float) -> bool:
    """
    clear message cache, as it is not possible to related.
    """
    return now - update_time > messages_cache_time


@app.post("/chat")
async def chat(item: Item):
    global messages

    # new session
    if item.content == 'p':
        messages = []
        return {"txt": ""}

    # clear cache
    now_timestamp = time.time()
    global messages_update_timestamp
    if clear_messages_session(messages_update_timestamp, now_timestamp):
        messages = []
    messages.append({"role": "user", "content": item.content})
    messages_update_timestamp = now_timestamp

    try:
        completion = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=messages
        )
    except openai.error.APIConnectionError as ex:
        traceback.print_exception(type(ex), ex, ex.__traceback__)
        return {"txt": "连接openai错误，请重试"}

    chat_response = completion.choices[0].message.content
    messages.append({"role": "assistant", "content": chat_response})

    return {"txt": chat_response}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8080)
