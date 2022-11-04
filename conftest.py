import pytest
from django.test import Client
from password_manager_app.models import LoginData, SupportContact, User, CreditCard


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def user_1(db):
    user = User.objects.create(
        username="test1",
        password="secretpassword",
        first_name="pantest",
        last_name="test2",
        email="kamil146532@wp.pl",
        is_staff=False,
        is_superuser=False,
        is_active=True,
    )
    return user


@pytest.fixture
def user_2(db):
    user = User.objects.create(
        username="test1",
        password="secretpassword2",
        first_name="pantest2",
        last_name="test22",
        email="kamil1465312@wp.pl",
        is_staff=False,
        is_superuser=False,
        is_active=True,
    )
    return user


@pytest.fixture
def login_data(db, user_1):
    login_data = LoginData.objects.create(data_name="fb", login_name="xx", email="conax13@gmail.com",
                                          password="123", url="https://www.facebook.com",
                                          login_data_group="Mail Account", user=user_1)

    return login_data


@pytest.fixture()
def support_contact():
    support_contact = SupportContact.objects.create(topic="1", sender_name="2", message_text="3")
    return support_contact
