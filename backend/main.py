from fastapi import FastAPI
from pydantic import BaseModel


from config import settings
from formatter import FormatterClass

app = FastAPI()

class Message(BaseModel):
    text: str

@app.post("/new-message/")
def create_message(message: Message):
    formatter = FormatterClass(
        iam_token=settings.API_KEY,
        folder_id=settings.FOLDER_ID,
        user_message=message.text
    )
    message_formatted = formatter.format()
    return {"message_formatted": message_formatted}