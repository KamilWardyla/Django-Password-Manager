import pytest
from django.urls import reverse
from password_manager_app.models import LoginData, SupportContact, User, CreditCard, SecretNote

"""Home View Test"""


@pytest.mark.django_db
def test_home_view(client):
    response = client.get(reverse('home'))
    assert response.status_code == 200


"""Register Test"""


def test_register_view(client):
    response = client.get(reverse('register'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_1(user_1):
    assert len(User.objects.all()) == 1
    assert User.objects.get(username="test1") == user_1


@pytest.mark.django_db
def test_user_2(user_2):
    assert len(User.objects.all()) == 1
    assert User.objects.get(username="test2") == user_2
    assert user_2.is_staff is True


"Add login data test"


@pytest.mark.django_db
def test_add_login_data(client, user_1, login_data):
    client.force_login(user_1)
    response = client.get(reverse('add_login_data'))
    assert response.status_code == 200
    assert LoginData.objects.get(data_name="fb") == login_data


"""LoginDataEditView test"""


def test_update_login_data(login_data, client, user_1):
    client.force_login(user_1)
    response = client.get(reverse('edit_login_data', kwargs={"id": login_data.id}))
    assert response.status_code == 200


"""RESPONSE STATUS CODE SHOULD BE 302 BECAUSE NOT AUTH USER SHOULD BE REDIRECT TO THE LOGIN PAGE"""


def test_update_login_data_user_not_auth(login_data, client, user_1):
    response = client.get(reverse('edit_login_data', kwargs={"id": login_data.id}))
    assert response.status_code == 302
    assert response['Location'] == f'/login/?next=/edit_login_data/{login_data.id}'


@pytest.mark.django_db
def test_update_login_data(login_data):
    login_data.data_name = "yt"
    login_data.save()
    new_login_data = LoginData.objects.get(data_name="yt")
    assert new_login_data.data_name == "yt"


"""LoginDataDelete test"""


@pytest.mark.djano_db
def test_delete_login_data(login_data, client, user_1):
    client.force_login(user_1)
    response = client.get(reverse('delete_login_data', kwargs={"id": login_data.id}))
    assert response.status_code == 200
    response_post = client.post(reverse('delete_login_data', kwargs={"id": login_data.id}))
    login_data.delete()
    assert response_post.status_code == 302
    assert response_post['Location'] == '/all_login_data/'


def test_delete_login_data_user_not_auth(login_data, client, user_1):
    response = client.get(reverse('delete_login_data', kwargs={"id": login_data.id}))
    assert response.status_code == 302
    response_post = client.post(reverse('delete_login_data', kwargs={"id": login_data.id}))
    assert response_post.status_code == 302
    assert response['Location'] == f'/login/?next=/delete_login_data/{login_data.id}'


"""LoginAllDataView test"""


@pytest.mark.django_db
def test_all_login_data(login_data, client, user_1):
    client.force_login(user_1)
    response = client.get(reverse("all_login_data"))
    assert response.status_code == 200
    assert len(LoginData.objects.all()) == 1


@pytest.mark.django_db
def test_all_login_data_user_not_auth(login_data, client):
    response = client.get(reverse("all_login_data"))
    assert response.status_code == 302
    assert response['Location'] == '/login/?next=/all_login_data/'


"""LoginData test"""


@pytest.mark.django_db
def test_login_data(login_data, client, user_1):
    client.force_login(user_1)
    response = client.get(reverse('login_data', kwargs={"id": login_data.id}))
    assert response.status_code == 200
    assert login_data.data_name == "fb"
    assert login_data.login_name == "xx"
    assert login_data.email == "conax13@gmail.com"
    assert login_data.password == "123"
    assert login_data.user == user_1


@pytest.mark.django_db
def test_login_data_user_not_auth(login_data, client):
    response = client.get(reverse('login_data', kwargs={"id": login_data.id}))
    assert response.status_code == 302
    assert response['Location'] == f'/login/?next=/login_data/{login_data.id}'


@pytest.mark.django_db
def test_login_data_user_not_owner(login_data, client, user_2):
    client.force_login(user_2)
    response = client.get(reverse('login_data', kwargs={"id": login_data.id}))
    assert response.status_code == 403


"""Add Credit Card test"""


@pytest.mark.django_db
def test_credit_card_add(client, user_1):
    client.force_login(user_1)
    response = client.get(reverse("add_credit_card"))
    assert response.status_code == 200
    response_post = client.post(reverse("add_credit_card"),
                                {"card_number": "1234567890123458", "expiration_date": "2022-02-13",
                                 "card_type": "Visa", "cvv": "123"})
    response_post.status_code = 200


@pytest.mark.django_db
def test_credit_card_add_user_not_auth(client):
    response = client.get(reverse("add_credit_card"))
    assert response.status_code == 302
    assert response['Location'] == '/login/?next=/add_credit_card/'


"""Edit credit card test"""


@pytest.mark.django_db
def test_edit_credit_card(client, credit_card, user_1):
    client.force_login(user_1)
    response = client.get(reverse('edit_credit_card', kwargs={'id': credit_card.id}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_edit_credit_card_user_not_auth(client, credit_card, user_1):
    response = client.get(reverse('edit_credit_card', kwargs={'id': credit_card.id}))
    assert response.status_code == 302
    assert response['Location'] == f'/login/?next=/edit_credit_card/{credit_card.id}'


@pytest.mark.django_db
def test_edit_credit_card_user_not_owner(client, credit_card, user_2):
    client.force_login(user_2)
    response = client.get(reverse('edit_credit_card', kwargs={'id': credit_card.id}))
    assert response.status_code == 403


@pytest.mark.django_db
def test_edit_credit_card2(credit_card):
    credit_card.cvv = "234"
    credit_card.save()
    credit_card_new_cvv = CreditCard.objects.get(id=credit_card.id)
    assert credit_card.cvv == credit_card_new_cvv.cvv


"""Delete credit card test"""


@pytest.mark.django_db
def test_delete_credit_card(credit_card, client, user_1):
    client.force_login(user_1)
    response = client.get(reverse('delete_credit_card', kwargs={"id": credit_card.id}))
    assert response.status_code == 200
    response_post = client.post(reverse('delete_credit_card', kwargs={"id": credit_card.id}))
    assert response_post.status_code == 302
    assert response_post['Location'] == '/credit_cards/'


@pytest.mark.django_db
def test_delete_credit_card_user_not_auth(credit_card, client):
    response = client.get(reverse('delete_credit_card', kwargs={"id": credit_card.id}))
    assert response.status_code == 302
    response_post = client.post(reverse('delete_credit_card', kwargs={"id": credit_card.id}))
    assert response_post.status_code == 302
    assert response['Location'] == f'/login/?next=/delete_credit_card/{credit_card.id}'


"All credit cards view test"


@pytest.mark.django_db
def test_all_credit_cards(credit_card, client, user_1):
    client.force_login(user_1)
    response = client.get(reverse('credit_cards'))
    assert response.status_code == 200
    assert len(CreditCard.objects.all()) == 1


@pytest.mark.django_db
def test_all_credit_cards_user_not_auth(client):
    response = client.get(reverse('credit_cards'))
    assert response.status_code == 302
    assert response['Location'] == '/login/?next=/credit_cards/'


"""Credit Card View test"""


@pytest.mark.django_db
def test_credit_card(credit_card, client, user_1):
    client.force_login(user_1)
    response = client.get(reverse('credit_card', kwargs={"id": credit_card.id}))
    assert response.status_code == 200
    assert credit_card.card_number == "1234567890123456"
    assert credit_card.expiration_date == "2022-02-13"
    assert credit_card.card_type == "Visa"
    assert credit_card.cvv == "123"
    assert credit_card.user == user_1


@pytest.mark.django_db
def test_credit_card_user_not_auth(credit_card, client):
    response = client.get(reverse('credit_card', kwargs={"id": credit_card.id}))
    assert response.status_code == 302
    assert response['Location'] == f'/login/?next=/credit_card/{credit_card.id}'


@pytest.mark.django_db
def test_credit_card_user_not_owner(credit_card, client, user_2):
    client.force_login(user_2)
    response = client.get(reverse('credit_card', kwargs={"id": credit_card.id}))
    assert response.status_code == 403


"""Secret Note Add test"""


@pytest.mark.django_db
def test_secret_note_add(client, user_1):
    client.force_login(user_1)
    response = client.get(reverse('secret_note_add'))
    assert response.status_code == 200
    response_post = client.post(reverse('secret_note_add'), {"note_name": "name2", "note_text": "text2"})
    response_post.status_code == 200
    new_secret_note = SecretNote.objects.get(note_name="name2")
    assert new_secret_note.note_text == "text2"


@pytest.mark.django_db
def test_secret_note_add_user_not_auth(client):
    response = client.get(reverse('secret_note_add'))
    assert response.status_code == 302
    assert response['Location'] == '/login/?/secret_note/=/secret_note_add/'


"""Edit Secret Note"""


@pytest.mark.django_db
def test_edit_secret_note(client, secret_note, user_1):
    client.force_login(user_1)
    response = client.get(reverse('edit_secret_note', kwargs={"id": secret_note.id}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_edit_secret_note_user_not_auth(client, secret_note):
    response = client.get(reverse('edit_secret_note', kwargs={"id": secret_note.id}))
    assert response.status_code == 302
    assert response['Location'] == f'/login/?next=/edit_secret_note/{secret_note.id}'


@pytest.mark.django_db
def test_edit_secret_note_user_not_owner(client, secret_note, user_2):
    client.force_login(user_2)
    response = client.get(reverse('edit_secret_note', kwargs={"id": secret_note.id}))
    assert response.status_code == 403


@pytest.mark.django_db
def test_edit_secret_note2(secret_note):
    secret_note.note_name = "name23"
    secret_note.save()
    new_secret_note_name = SecretNote.objects.get(id=secret_note.id)
    assert secret_note.note_name == "name23"
    assert new_secret_note_name.note_name == secret_note.note_name


"""Delete Secret Note test"""


@pytest.mark.django_db
def test_delete_secret_note(client, secret_note, user_1):
    client.force_login(user_1)
    response = client.get(reverse("delete_secret_note", kwargs={"id": secret_note.id}))
    assert response.status_code == 200
    response_post = client.post(reverse("delete_secret_note", kwargs={"id": secret_note.id}))
    assert response_post.status_code == 302
    assert response_post['Location'] == '/notes/'


@pytest.mark.django_db
def test_delete_secret_note_user_not_auth(client, secret_note):
    response = client.get(reverse("delete_secret_note", kwargs={"id": secret_note.id}))
    assert response.status_code == 302
    response_post = client.post(reverse("delete_secret_note", kwargs={"id": secret_note.id}))
    assert response_post.status_code == 302
    assert response['Location'] == f'/login/?next=/delete_secret_note/{secret_note.id}'


@pytest.mark.django_db
def test_delete_secret_note_user_not_owner(client, secret_note, user_2):
    client.force_login(user_2)
    response = client.get(reverse('delete_secret_note', kwargs={"id": secret_note.id}))
    assert response.status_code == 403


"""All Secret Notes View Test"""


@pytest.mark.django_db
def test_all_secret_notes(client, user_1):
    client.force_login(user_1)
    response = client.get(reverse('my_notes'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_all_secret_notes_user_not_auth(client):
    response = client.get(reverse('my_notes'))
    assert response.status_code == 302
    assert response['Location'] == '/login/?next=/notes/'


"""Secret Note View Test"""


@pytest.mark.django_db
def test_secret_note(secret_note, client, user_1):
    client.force_login(user_1)
    response = client.get(reverse("secret_note", kwargs={"id": secret_note.id}))
    assert response.status_code == 200
    assert secret_note.note_name == "name"
    assert secret_note.note_text == "text"
    assert secret_note.user == user_1


@pytest.mark.django_db
def test_secret_note_user_not_auth(client, secret_note):
    response = client.get(reverse("secret_note", kwargs={"id": secret_note.id}))
    assert response.status_code == 302
    assert response['Location'] == f'/login/?next=/secret_note/{secret_note.id}'


@pytest.mark.django_db
def test_secret_note_user_not_owner(client, secret_note, user_2):
    client.force_login(user_2)
    response = client.get(reverse("secret_note", kwargs={"id": secret_note.id}))
    assert response.status_code == 403


"""Add support contact Test"""


@pytest.mark.django_db
def test_add_support_contact(support_contact):
    assert len(SupportContact.objects.all()) == 1
    assert SupportContact.objects.get(topic="1") == support_contact


@pytest.mark.django_db
def test_add_support_contact_view(client):
    response = client.get(reverse('support_contact'))
    assert response.status_code == 200
    response_post = client.post(reverse('support_contact'),
                                {"topic": "topic2", "sender_email": "www@wp.pl", "message_text": "text"})
    assert response_post.status_code == 302
    new_support_case = SupportContact.objects.get(topic="topic2")
    assert new_support_case.message_text == "text"


"""All support cases Test"""


@pytest.mark.django_db
def test_all_support_cases(client, support_contact, user_2):
    client.force_login(user_2)
    response = client.get(reverse("support_cases"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_all_support_cases_user_is_not_staff(client, support_contact, user_1):
    client.force_login(user_1)
    response = client.get(reverse("support_cases"))
    assert response.status_code == 403


"""Support Case Test"""


@pytest.mark.django_db
def test_support_case(client, support_contact, user_2):
    client.force_login(user_2)
    response = client.get(reverse('support_case', kwargs={"id": support_contact.id}))
    assert response.status_code == 200
    assert support_contact.topic == "1"
    assert support_contact.sender_email == "www@wp.pl"
    assert support_contact.message_text == "3"


@pytest.mark.django_db
def test_support_case_user_is_not_staff(client, support_contact, user_1):
    client.force_login(user_1)
    response = client.get(reverse('support_case', kwargs={"id": support_contact.id}))
    assert response.status_code == 403


"""Support Case Delete Test"""


@pytest.mark.django_db
def test_delete_support_case(client, support_contact, user_2):
    client.force_login(user_2)
    response = client.get(reverse('delete_support_case', kwargs={"id": support_contact.id}))
    assert response.status_code == 200
    response_post = client.post(reverse('delete_support_case', kwargs={"id": support_contact.id}))
    assert response_post.status_code == 302
    assert response_post['Location'] == '/support_cases/'


@pytest.mark.django_db
def test_delete_support_case_user_is_not_staff(client, support_contact, user_1):
    client.force_login(user_1)
    response = client.get(reverse('delete_support_case', kwargs={"id": support_contact.id}))
    assert response.status_code == 403
    response_post = client.post(reverse('delete_support_case', kwargs={"id": support_contact.id}))
    assert response_post.status_code == 403
