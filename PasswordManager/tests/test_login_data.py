import pytest
from django.urls import reverse
from password_manager_app.models import SupportContact


@pytest.mark.django_db
def test_add_login_data(client):
    login_data = SupportContact.objects.create(topic="a", sender_name='b', message_text='3')
