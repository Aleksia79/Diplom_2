import requests
from allure import step
from src.config import Config


class OrdersApi:

    def __init__(self, url_endpoint, user_name=None, response_create=None, order_id=None, order_number=None,
                 ingredients=None, ingredients_used=None, response_get_user_orders=None, user_orders_id=None):
        self.url_endpoint = url_endpoint
        # ингредиенты до заказа
        self.ingredients = ingredients
        self.response_create = response_create
        self.order_id = order_id
        self.user_name = user_name
        self.order_number = order_number
        # ингредиенты в заказе
        self.ingredients_used = ingredients_used
        self.response_get_user_orders = response_get_user_orders
        self.user_orders_id = user_orders_id

    # создание заказа
    @step(f'Отправляем POST-запрос с параметром "ingredients" и c "access_token" в хедере для создания заказа на ручку '
          f'{Config.ORDERS}')
    def create_order(self, user_name, access_token, ingredients):
        headers = {"authorization": access_token}
        self.ingredients = ingredients
        ingredients_set = {"ingredients": ingredients}
        self.response_create = requests.post(self.url_endpoint, headers=headers, json=ingredients_set)
        if self.response_create.status_code == 500:
            return self.response_create
        if self.response_create.json()["success"] is True and "ingredients" in self.response_create.json()["order"].keys():
            self.ingredients_used = []
            for i in self.response_create.json()["order"]["ingredients"]:
                self.ingredients_used.append(i["_id"])
            self.order_id = self.response_create.json()["order"]["_id"]
            self.user_name = user_name
        if self.response_create.json()["success"] is True:
            self.order_number = self.response_create.json()["order"]["number"]
        return self.response_create

    # получение заказов конкретного пользователя
    @step(f'Отправляем GET-запрос с "access_token" в хедере для получения заказа конкретного пользователя на ручку '
          f'{Config.ORDERS}')
    def get_user_orders(self, access_token):
        headers = {"authorization": access_token}
        self.response_get_user_orders = requests.get(self.url_endpoint, headers=headers)
        if self.response_get_user_orders.json()["success"] is True:
            self.user_orders_id = []
            for i in self.response_get_user_orders.json()["orders"]:
                self.user_orders_id.append(i["_id"])
        return self.response_get_user_orders

    # удаление заказа
    # в API документации нет удаления заказа
