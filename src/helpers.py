import faker
from allure import step
from random import randint
import string
import random


# генерация email, пароля и имени
def generate_user_data(email=None, password=None, name=None):
    fake = faker.Faker()
    if email != "":
        email = f'{"".join(chr(randint(97, 122)) for _ in range(7))}{fake.email()}'
    if password != "":
        password = fake.password(length=randint(6, 10))
    if name != "":
        name = fake.name()
    return email, password, name


@step('Генерируем ингредиенты с неверным хешем')
def generate_id_ingredients():
    characters = string.digits + string.ascii_lowercase
    return [''.join(random.choices(characters, k=24)), ''.join(random.choices(characters, k=24))]


@step('Генерируем незарегистрированный email')
def generate_email():
    fake = faker.Faker()
    email = f'{"".join(chr(randint(97, 122)) for _ in range(7))}{fake.email()}'
    return email


@step('Генерируем незарегистрированный пароль')
def generate_password():
    fake = faker.Faker()
    password = fake.password(length=randint(6, 10))
    return password


@step('Генерируем незарегистрированное имя')
def generate_name():
    fake = faker.Faker()
    name = fake.name()
    return name
