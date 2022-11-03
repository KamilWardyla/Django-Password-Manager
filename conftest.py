import pytest
from django.test import Client
from password_manager_app.models import LoginData


@pytest.fixture
def login_data():
    login_data = LoginData.objects.create(data_name="fb", login_name="xx", email="conax13@gmail.com",
                                          password="123", url="https://www.facebook.com",
                                          login_data_group="Mail Account",
                                          user="1")
    return login_data
