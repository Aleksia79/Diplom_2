from allure import title, step
from src.helpers import *


class TestUserLogin:

    @title('Проверяем, что авторизация существующего пользователя возвращает правильные код и тело ответа')
    def test_user_login_true(self, create_user_and_return_object):
        user = create_user_and_return_object
        response_login = user.user_login(user.email, user.password)
        with step('ОР: запрос возвращает код ответа 201'):
            assert response_login.status_code == 200
        with (step('ОР: в теле ответа на запрос получаем {"success": True}, а также email и name')):
            assert (response_login.json()["success"] is True
                    and response_login.json()["user"] == {"email": user.email, "name": user.name})

    @title('Проверяем, что авторизация c неверными логином и паролем возвращает правильные код и тело ответа')
    def test_user_login_incorrect_data_true(self, user_api):
        user = user_api
        email = generate_email()
        password = generate_password()
        response_login = user.user_login(email, password)
        with step('ОР: запрос возвращает код ответа 401'):
            assert response_login.status_code == 401
        with step('ОР: в теле ответа на запрос получаем {"success": True}, а также "message": "email or password are '
                  'incorrect"'):
            assert response_login.json() == {"success": False,
                                             "message": "email or password are incorrect"
                                             }
