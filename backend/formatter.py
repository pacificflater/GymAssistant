import requests

URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

prompt = "Тренер присылает упражнения на три дня в виде списка"\
         " Нужно отформатировать список для obsidian следующим образом"\
         "К каждому упражнению добавить параметр 'Группа мышц' в формате Группа мышц:: Кор"\
         "Вот массив из доступных вариантов ['Ноги', 'Грудь', 'Спина', 'Плечи', 'Бицепс', 'Трицепс', 'Кор', 'Другое']"\
         "Привести его к формату"\
         "- **Пресс с мячом, ноги бабочкой**:"\
         "	- Вес:: 11 кг"\
         "	- Подходы:: 4"\
         "	- Повторения:: 15"\
         "	- Группа мышц:: Кор"\
         "Добавить в раздел #### Упражнения, не оставляй пустые строки"\
         "Еще для того чтобы предоставлять тренеру отчет о тренировках мне нужно отдельным списком перечислить названия упражнений, рядом с которыми я уже потом буду подставлять результаты в формате: 1. Название упражнения:"\
         "Сделай оглавление #### Результат"\
         "Если в названии упражнений присутствуют запятые, удали их"\
         "Замени 'ё' на 'е'"\
         "Если в названии присутствуют веса или повторения по типу 3х12 не включай их в название"\
         "Результат предоставь в markdown формате для obsidian "\
         "Если в сообщении несколько тренировок разбей на отдельные markdown заметки"

class FormatterClass:

    def __init__(self, iam_token, folder_id, user_message):
        self.iam_token = iam_token
        self.folder_id = folder_id
        self.user_message = user_message

    def format(self):

        # Собираем запрос
        data = {}
        # Указываем тип модели
        data["modelUri"] = f"gpt://{self.folder_id}/yandexgpt"
        # Настраиваем опции
        data["completionOptions"] = {"temperature": 0.3, "maxTokens": 1000}
        # Указываем контекст для модели
        data["messages"] = [
            {"role": "system",
             "text": f"{prompt}"},
            {"role": "user",
             "text": f"{self.user_message}"},
        ]

        # Отправляем запрос
        try:
            response = requests.post(
                "https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
                headers={
                    "Accept": "application/json",
                    "Authorization": f"Bearer {self.iam_token}"
                },
                json=data,
                timeout=30
            )
            response.raise_for_status()
            response_data = response.json()

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к API: {e}")
            return
        except ValueError as e:
            print(f"Ошибка при парсинге JSON ответа: {e}")
            return

        # Извлекаем текст ответа
        if "result" in response_data and "alternatives" in response_data["result"]:
            result_text = response_data["result"]["alternatives"][0]["message"]["text"]
            return result_text