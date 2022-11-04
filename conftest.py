import pytest
from password_manager_app.models import LoginData, SupportContact, User, CreditCard, SecretNote
from django.test import Client


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
        username="test2",
        password="secretpassword2",
        first_name="pantest2",
        last_name="test22",
        email="kamil1465312@wp.pl",
        is_staff=True,
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


@pytest.fixture
def credit_card(db, user_1):
    credit_card = CreditCard.objects.create(card_number="1234567890123456", expiration_date="2022-02-13",
                                            card_type="Visa", cvv="123", user=user_1)
    return credit_card


@pytest.fixture
def secret_note(db, user_1):
    secret_note = SecretNote.objects.create(note_name="name", note_text="text", user=user_1)
    return secret_note


@pytest.fixture
def support_contact(db):
    support_contact = SupportContact.objects.create(topic="1", sender_email="www@wp.pl", message_text="3")
    return support_contact
