from allure import title, step
from src.data import Data


class TestUserOrders:

    @title('Проверяем, что успешное получение заказов конкретного пользователя возвращает правильные '
           'код и тело ответа')
    def test_get_users_orders_true(self, create_user_and_return_object, order_api):
        user = create_user_and_return_object
        order = order_api
        order.create_order(user.name, user.access_token, Data.INGREDIENTS)
        response_get_user_orders = order.get_user_orders(user.access_token)
        with step('ОР: запрос возвращает код ответа 200'):
            assert response_get_user_orders.status_code == 200
        with step(f'ОР: в теле ответа на запрос получаем "success": True, а также проверяем, что id заказа, '
                  f'полученный при его создании пользователем, совпадает с id заказа в полученном списке заказов '
                  f'пользователя'):
            assert (order.response_get_user_orders.json()["success"] is True and order.order_id in order.user_orders_id)

    @title('Проверяем, что получение заказов конкретного пользователя без авторизации возвращает правильные '
           'код и тело ответа')
    def test_get_users_orders_without_token_true(self, create_user_and_return_object, order_api):
        user = create_user_and_return_object
        order = order_api
        order.create_order(user.name, user.access_token, Data.INGREDIENTS)
        response_get_user_orders = order.get_user_orders(None)
        with step('ОР: запрос возвращает код ответа 401'):
            assert response_get_user_orders.status_code == 401
        with (step(f'ОР: в теле ответа на запрос получаем "success": False и "message": "You should be authorised"')):
            assert order.response_get_user_orders.json() == {"success": False,
                                                             "message": "You should be authorised"
                                                             }
