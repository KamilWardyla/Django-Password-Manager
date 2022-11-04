import pytest
from django.urls import reverse
from password_manager_app.models import LoginData, SupportContact, User, CreditCard

"""Register Test"""


@pytest.mark.django_db
def test_user_1(user_1):
    assert len(User.objects.all()) == 1
    assert User.objects.get(username="test1") == user_1


@pytest.mark.django_db
def test_home_view(client):
    response = client.get(reverse('home'))
    assert response.status_code == 200
"Add login data test"


@pytest.mark.django_db
def test_add_login_data(login_data):
    assert LoginData.objects.get(data_name="fb") == login_data


@pytest.mark.django_db
def test_update_login_data(login_data):
    login_data.data_name = "yt"
    login_data.save()
    new_login_data = LoginData.objects.get(data_name="yt")
    assert new_login_data.data_name == "yt"


# @pytest.mark.djano_db
# def test_delete_login_data(login_data):
#     login_data.delete()
#     assert login_data.exists() == False


@pytest.mark.django_db
def test_login_data_details(login_data):
    assert len(LoginData.objects.all()) == 1


"""Add support contact"""


@pytest.mark.django_db
def test_add_support_contact(support_contact):
    assert len(SupportContact.objects.all()) == 1
    assert SupportContact.objects.get(topic="1") == support_contact


@pytest.mark.django_db
def credit_card_add(client, user_1):
    client.login(user_1)
    response = client.post(reverse("add_credit_card"),
                           {"card_number": "1234567890123456", "expiration_date": "2022-12-04", "card_type": "Visa",
                            "cvv": "123"})
    assert response.status_code == 302
    assert len(CreditCard.objects.all()) == 1


def test_details(client, user_1):
    client.force_login(user_1)
    response = client.get(reverse("all_login_data"))
    assert response.status_code == 200
