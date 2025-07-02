from allure import title, step
from src.helpers import *
from src.data import Data


class TestCreateOrder:

    @title('Проверяем, успешное создание заказа под авторизованным пользователем возвращает правильные код и тело '
           'ответа')
    def test_create_order_true(self, create_order_and_return_object):
        order = create_order_and_return_object
        with step('ОР: запрос возвращает код ответа 200'):
            assert order.response_create.status_code == 200
        with step(f'ОР: в теле ответа на запрос получаем "success": True, а также name: {order.user_name} и'
                  f' uuid переданных ингредиентов: {Data.INGREDIENTS}'):
            assert (order.response_create.json()["success"] is True and order.ingredients_used ==
                    order.ingredients and order.response_create.json()["order"]["owner"]["name"] == order.user_name)

    @title('Проверяем, что заказ без авторизации пользователя возвращает правильные код и тело '
           'ответа')
    def test_create_order_without_token_true(self, order_api):
        order = order_api
        order.create_order(None, None, Data.INGREDIENTS)
        with step('ОР: запрос возвращает код ответа 200'):
            assert order.response_create.status_code == 200
        with step(f'ОР: в теле ответа на запрос получаем "success": True, а также название бургера и номер заказа'):
            assert order.response_create.json() == {"success": True,
                                                    "name": "Бессмертный флюоресцентный бургер",
                                                    "order": {
                                                        "number": order.order_number
                                                    }
                                                    }

    @title('Проверяем, что заказ без ингредиентов возвращает правильные код и тело '
           'ответа')
    def test_create_order_without_ingredients_true(self, create_user_and_return_object, order_api):
        user = create_user_and_return_object
        order = order_api
        order.create_order(user.name, user.access_token, None)
        with step('ОР: запрос возвращает код ответа 400'):
            assert order.response_create.status_code == 400
        with step(f'ОР: в теле ответа на запрос получаем "success": False, а также "message": "Ingredient ids must '
                  f'be provided"'):
            assert order.response_create.json() == {"success": False,
                                                    "message": "Ingredient ids must be provided"
                                                    }

    @title('Проверяем, что заказ c неверным хешем ингредиентов возвращает правильные код и тело '
           'ответа')
    def test_create_order_with_wrong_ingredients_true(self, create_user_and_return_object, order_api):
        user = create_user_and_return_object
        order = order_api
        order.create_order(user.name, user.access_token, generate_id_ingredients())
        with step('ОР: запрос возвращает код ответа 500'):
            assert order.response_create.status_code == 500

