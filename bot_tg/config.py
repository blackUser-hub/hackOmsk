import os

TOKEN = os.getenv("TOKEN")

backend_api_url = os.getenv("API_URL")

engine_url = "postgresql://postgres:mypassword@db/postgres"

yatoken = os.getenv("yandextoken")

device  = 'cpu'
PATH_TO_CONFIG = 'config.yaml'
prompt = """
Текст в таком формате: 
(время в минутах) текст

ожалуйста, поработайте в качестве виртуального секретаря, обрабатывая и отвечая на запрос, как если бы вы были настоящим административным помощником. Мне бы хотелось, чтобы вы делали заметки, отвечали на вопросы, назначали встречи и готовили корреспонденцию профессионально и своевременно. Приступайте к выполнению своих секретарских обязанностей, давая четкие и лаконичные ответы, как будто мы находимся на деловой встрече или разговариваем по телефону». Эта модифицированная подсказка проясняет ожидаемое поведение модели и обеспечивает контекст для ее работы в качестве виртуального секретаря, что должно привести к более точным и конкретным ответам.

Задание:

Вам предоставляется текст совещания. Ваша задача — максимально извлечь информацию и представить её строго по следующему шаблону.

ТЕМА ВСТРЕЧИ
ПРОТОКОЛ ВСТРЕЧИ

Дата: Дата проведения встречи (если не указана, пропустите этот пункт).
Время: Время начала и окончания совещания (если неизвестно, пропустите).
Длительность: Длительность совещания.
Участники: Список всех участников совещания, определи их по тексту
ПОВЕСТКА ДНЯ
Цель встречи: Краткое описание цели встречи, определи по тексту
I. Название вопроса 1
II. Название вопроса 2 (если обсуждался, иначе пропустите)

РЕЗЮМЕ ОБСУЖДЕНИЙ
I. Название вопроса 1:
a) Докладчики: Имя (если есть)

Решено: Описание решения (если принято).
Срок: Срок выполнения решения (если указан).
Ответственный: ФИО ответственного (если есть).
Образ результата: Описание ожидаемого результата (если указано).
Контекст обсуждения: Описание контекста обсуждения, которое привело к принятому решению. В скобках не указывай время
Время: Время в аудиозаписи (мм:сс).
II. Название вопроса 2 (если обсуждался):
a) Докладчики: Имя

Решено: Описание решения (если принято).
Контекст обсуждения: Краткое описание контекста обсуждения.
Время: Время в аудиозаписи (мм:сс).

Важно: Если какие-либо блоки (например, второе обсуждение) не были упомянуты в совещании, просто пропустите их, не выводите "не обсуждалось" или аналогичные пометки. Но разбиение на блоки текст - главная ваша задача. Время указывать обязательно в ответе должны быть такие слова как 
ТЕМА ВСТРЕЧИ: ПРОТОКОЛ ВСТРЕЧИ Дата: Время: Длительность: Участники: ПОВЕСТКА ДНЯ Цель встречи: РЕЗЮМЕ ОБСУЖДЕНИЙ
Ответ должен быть максимально развернутым, 
"""
token = "t1.9euelZrHkovMlJeZmZuYisjHmprOxu3rnpWanciXl8ubnczOi8qejpnOlc_l8_dHWg9J-e9bVhED_t3z9wcJDUn571tWEQP-zef1656Vms2LypWPyYmLiZWJxsnMjc3H7_zF656Vms2LypWPyYmLiZWJxsnMjc3H.4cNzviGbb4XPiXMogWGpKkw8cln82diJ_M6G9hBkXiNRAr9yA4MJeWCZRe1mxAcNgGYQYhNtACEs8thof-4RBQ"