from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os
from pathlib import Path

from config import settings
from formatter import FormatterClass

app = FastAPI()

# Получаем абсолютный путь к текущей директории
BASE_DIR = Path(__file__).resolve().parent

# Монтируем статические файлы с абсолютным путем
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# Настраиваем шаблоны с абсолютным путем
templates = Jinja2Templates(directory=BASE_DIR / "templates")


class Message(BaseModel):
    text: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Главная страница с формой"""
    return templates.TemplateResponse("form.html", {"request": request})


@app.post("/new-message/")
def create_message(message: Message):
    formatter = FormatterClass(
        iam_token=settings.API_KEY,
        folder_id=settings.FOLDER_ID,
        user_message=message.text
    )
    print(f"API KEY:{settings.API_KEY}")
    message_formatted = formatter.format()
    return {"message_formatted": message_formatted}


# Добавьте этот endpoint для обработки формы
@app.post("/submit-form")
async def submit_form(request: Request, text: str = Form(...)):
    """Endpoint для обработки HTML формы"""
    # Создаем сообщение и обрабатываем его
    message = Message(text=text)
    formatter = FormatterClass(iam_token=settings.API_KEY,
                               folder_id=settings.FOLDER_ID,
                               user_message=message.text
    )
    message_formatted = formatter.format()

    # Возвращаем результат
    return templates.TemplateResponse("result.html", {
        "request": request,
        "original_text": text,
        "formatted_text": message_formatted
    })


# Добавьте endpoint для отладки
@app.get("/debug")
async def debug_info():
    """Endpoint для отладки - проверяем пути"""
    return {
        "base_dir": str(BASE_DIR),
        "templates_exists": (BASE_DIR / "templates").exists(),
        "static_exists": (BASE_DIR / "static").exists(),
        "form_exists": (BASE_DIR / "templates" / "form.html").exists()
    }