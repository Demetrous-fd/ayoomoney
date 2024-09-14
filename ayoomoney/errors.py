class InvalidTokenError(Exception):
    def __init__(self):
        message = "Указанный токен не существует, либо отозван."
        super().__init__(message)


class CreateTokenError(Exception):
    def __init__(self, error: str):
        info = {
            "invalid_grant": "Обязательные параметры запроса отсутствуют или имеют некорректные или недопустимые значения.",
            "unauthorized_client": "Неверное значение параметра client_id или client_secret, либо приложение не имеет права запрашивать авторизацию (например, ЮMoney заблокировали его client_id).",
            "invalid_request": "В выдаче access_token отказано. ЮMoney не выдавали временный токен, токен просрочен, или по этому временному токену уже выдан access_token (повторный запрос токена авторизации с тем же временным токеном).",
        }
        message = "\n".join([
            f"Не удалось создать токен: {error=}",
            f"Описание ошибки: {info.get(error, 'Неизвестная ошибка')}"
        ])
        super().__init__(message)
