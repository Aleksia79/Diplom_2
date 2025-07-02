import pytest
from allure import title, step
from src.helpers import generate_user_data


class TestCreateUser:

    @title('Проверяем, что успешная регистрация пользователя возвращает правильные код и тело ответа')
    def test_create_user_true(self, create_user_and_return_object):
        user = create_user_and_return_object
        with step('ОР: запрос возвращает код ответа 201'):
            assert user.response_create.status_code == 200
        with step('ОР: в теле ответа на запрос получаем {"success": True}, а также email, name и токены'):
            assert user.response_create.json() == {"success": True,
                                                   "user": {
                                                       "email": user.email,
                                                       "name": user.name,
                                                   },
                                                   "accessToken": user.access_token,
                                                   "refreshToken": user.refresh_token
                                                   }

    @title('Проверяем, что нельзя создать двух одинаковых пользователей')
    def test_cant_create_user_repeat_true(self, create_user_and_return_object, user_api):
        user_1 = create_user_and_return_object
        with (step('Повторно передаем сгенерированные login, password, first_name курьера')):
            user_2 = user_api
            user_2.create_user(user_1.email, user_1.password, user_1.name)
        with step('ОР: запрос возвращает код ответа 403'):
            assert user_2.response_create.status_code == 403
        with step('ОР: в теле ответа на запрос получаем {"success": "false, "message": "User already exists"}'):
            assert user_2.response_create.json() == {"success": False,
                                                     "message": "User already exists"
                                                     }

    @title('Проверяем, что нельзя создать пользователя с пустым полем')
    @pytest.mark.parametrize('email, password, name', [("", "fake_pwd", "fake_name"),
                                                       ("fake_email", "", "fake_name"),
                                                       ("fake_email", "fake_pwd", "")])
    def test_cant_create_courier_empty_email_true(self, user_api, email, password, name):
        with step(f'Отправляем сгенерированные данные пользователя {email, password, name}, один параметр пустой'):
            user = user_api
            email, password, name = generate_user_data(email, password, name)
            user.create_user(email, password, name)
        with step('ОР: запрос возвращает код ответа 403'):
            assert user.response_create.status_code == 403
        with step('ОР: в теле ответа на запрос получаем {"success": "false, "message": "Email, password and name '
                  'are required fields"}'):
            assert user.response_create.json() == {"success": False,
                                                   "message": "Email, password and name are required fields"
                                                   }
