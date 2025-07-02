from allure import title, step
from src.helpers import *


class TestDataUserChange:

    @title('Проверяем, что успешное обновление данных пользователя возвращает правильные код и тело '
           'ответа')
    def test_data_user_change_true(self, create_user_and_return_object):
        user = create_user_and_return_object
        new_email = generate_email()
        new_name = generate_name()
        response_change = user.data_user_change(new_email, new_name, {"authorization": user.access_token})
        with step('ОР: запрос возвращает код ответа 200'):
            assert response_change.status_code == 200
        with step(f'ОР: в теле ответа на запрос получаем "success": True, а также новые email: {new_email} и name:'
                  f' {new_name}'):
            assert response_change.json() == {"success": True,
                                              "user": {
                                                  "email": new_email,
                                                  "name": new_name
                                              }
                                              }

    @title('Проверяем, что обновление данных пользователя без токена не успешно и возвращает правильные код и тело'
           'ответа')
    def test_data_user_change_without_token_true(self, create_user_and_return_object):
        user = create_user_and_return_object
        email = generate_email()
        name = generate_name()
        response_change = user.data_user_change(email, name, None)
        with step('ОР: запрос возвращает код ответа 401'):
            assert response_change.status_code == 401
        with step('ОР: в теле ответа на запрос получаем {"success": false, "message": "You should be authorised"}'):
            assert response_change.json() == {"success": False,
                                              "message": "You should be authorised"
                                              }
