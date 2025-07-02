from allure import step

import requests
from src.config import Config


class UserApi:

    def __init__(self, url, access_token=None, refresh_token=None, email=None, password=None, name=None,
                 response_create=None):
        self.url = url
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.email = email
        self.password = password
        self.name = name
        self.response_create = response_create

    # создание пользователя
    @step(f'Отправляем POST-запрос с параметрами "email", "password", "name" для создания user на ручку '
          f'{Config.CREATE_USER}')
    def create_user(self, email, password, name):
        user_data = {"email": email, "password": password, "name": name}
        self.response_create = requests.post(self.url + Config.CREATE_USER, json=user_data)
        self.email = email
        self.password = password
        self.name = name
        if "accessToken" in self.response_create.json():
            self.access_token = self.response_create.json()["accessToken"]
        if "refreshToken" in self.response_create.json():
            self.refresh_token = self.response_create.json()["refreshToken"]
        return self.response_create

    # логин пользователя
    @step(f'Отправляем POST-запрос с параметрами "email" и "password", "name" для авторизации пользователя на ручку '
          f'{Config.USER_LOGIN}')
    def user_login(self, email, password):
        user_data = {"email": email, "password": password}
        response_login = requests.post(self.url + Config.USER_LOGIN, json=user_data)
        return response_login

    # изменение данных пользователя c авторизацией
    @step(f'Отправляем PATCH-запрос с параметрами "email" и "name" а также с "access_token" в хедере для изменения '
          f'данных пользователя на ручку {Config.DATA_USER_CHANGE}')
    def data_user_change(self, email, name, headers):
        data_user = {"email": email, "name": name}
        response_change = requests.patch(self.url + Config.DATA_USER_CHANGE, headers=headers, json=data_user)
        return response_change

    # удаление пользователя
    def delete_user(self):
        if self.access_token is not None:
            with step(f'Удаление пользователя с токеном {self.access_token}'):
                response_delete = requests.delete(self.url + Config.DATA_USER_CHANGE, headers={
                    "Authorization": self.access_token})
            with step(f'Запрос на удаление пользователя выполнен со статус-кодом: {response_delete.status_code}'):
                pass
            return response_delete
        with step('Пользователь не найден'):
            pass
