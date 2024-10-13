# Пример использования ayoomoney в телеграм боте

## Описание

В этом примере реализован телеграм бот для приёма платежей через yoomoney с ручной и автоматической проверкой оплаты.

## Используемые библиотеки

- aiogram v3
- SQLAlchemy
- Alembic
- fastapi (Используется для получения уведомлений от yoomoney)
- faststream (Используется для обмена сообщениями)
- dependency-injector (Используется для внедрения зависимостей)

## Содержимое каталогов

- notify -> Web-сервер используется для получения уведомлений от yoomoney и отправки полученных данных боту через брокер
  сообщений
- migration -> Миграции для создания БД
- bot -> Телеграм бот

```tree
bot
├───broker - обработчики брокера сообщений
├───handlers - обработчики бота
├───keyboards
├───models - описание моделей БД
├───repositories - доступ к данным и работа с БД
├───schemes - описание моделей pydantic
└───containers.py - описание зависимостей
```

## Шаги для локального запуска

0. Установите [git](https://git-scm.com/), redis и [tuna](https://tuna.am/)
1. С клонируйте репозиторий

```shell
git clone https://github.com/Demetrous-fd/ayoomoney
```

2. Перейдите в директорию ayoomoney/examples/notification

```shell
cd ayoomoney/examples/notification
```

3. Создайте виртуальное окружение и установите зависимости
    - Windows
    ```shell
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    ```
    - Linux
    ```shell
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
4. Переименуйте файл .env.example в .env
    - Windows
    ```shell
    copy .env.example .env
    ```
    - Linux
    ```shell
    cp .env.example .env
    ```
5. Укажите переменные окружения в .env

```text
TELEGRAM_TOKEN=token
YOOMONEY_TOKEN=token
YOOMONEY_NOTIFICATION_SECRET=secret ; Пока пропустите

; Если у вас запущен redis не локально, укажите данные для подключения в REDIS_DSN
;REDIS_DSN=redis://username:password@193.3.168.217:6379/0
;REDIS_DSN=redis://193.3.168.217:6379
```

6. Запустите миграцию

```shell
alembic upgrade head
```

7. Запустите сервис уведомлений

```shell
uvicorn notify:app --port 8042
```

8. Откройте новую консоль и запустите туннель через tuna

```shell
tuna http 8042
```

9. Скопируйте адрес туннеля и добавьте к нему /notification/payment

```text
https://000000-0-000-000-00.ru.tuna.am/notification/payment
```

10. Перейдите на страницу [HTTP-уведомлений yoomoney](https://yoomoney.ru/transfer/myservices/http-notification)

- Укажите адрес туннеля
- Скопируйте "Секрет для проверки подлинности" и укажите его в файле .env (YOOMONEY_NOTIFICATION_SECRET)

11. Запустите бота

```shell
python -m bot
```

12. Выполните в боте команду /start, попробуйте создать тестовый платеж и оплатить его
