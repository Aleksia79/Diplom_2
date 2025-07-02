import pytest
from allure import title, step

from src.config import Config
from src.data import Data
from src.helpers import *
from src.orders_api import OrdersApi
from src.user_api import UserApi


@pytest.fixture()
@title('Создаем объект user')
def user_api():
    user = UserApi(Config.URL)
    yield user
    with step('Удаляем user'):
        user.delete_user()


@pytest.fixture()
@title('Создаем объект order')
def order_api():
    order = OrdersApi(Config.URL + Config.ORDERS)
    return order


@pytest.fixture()
@title('Генерируем данные user, регистрируем и возвращаем объект - user')
def create_user_and_return_object(user_api):
    with step('Генерируем email, password, name пользователя'):
        email, password, name = generate_user_data()
    user = user_api
    with step('Создаем пользователя по сгенерированным email, password, name'):
        user.create_user(email, password, name)
    with step(f'Получили access_token пользователя: {user.access_token}'):
        return user


# создание заказа c авторизацией
@pytest.fixture()
def create_order_and_return_object(create_user_and_return_object, order_api):
    user = create_user_and_return_object
    order = order_api
    order.create_order(user.name, user.access_token, Data.INGREDIENTS)
    return order


@pytest.fixture()
def faker_email():
    email = generate_email()
    return email


@pytest.fixture()
def faker_pwd():
    pwd = generate_password()
    return pwd


@pytest.fixture()
def faker_name():
    name = generate_name()
    return name
