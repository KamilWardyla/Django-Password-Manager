from django import forms
from .models import User
from django.forms import ModelForm
from .models import LoginData, SecretNote, SupportContact, CreditCard
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from datetime import date


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class LoginDataForm(ModelForm):
    url = forms.CharField(validators=[URLValidator], required=False)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = LoginData
        exclude = ['user']


class SecretNoteForm(ModelForm):
    class Meta:
        model = SecretNote
        exclude = ['user']


class SupportContactForm(ModelForm):
    class Meta:
        model = SupportContact
        fields = "__all__"


class CreditCardForm(ModelForm):
    @staticmethod
    def card_number_validator(value):
        if value.isdigit() is False or len(value) != 16:
            raise forms.ValidationError(
                "Only digital available and length 16 characters")

    @staticmethod
    def cvv_validator(value):
        if value.isdigit() is False or len(value) != 3:
            raise ValidationError(
                "Only digital available and length 3 characters")

    @staticmethod
    def date_validator(value):
        today = date.today()
        if value < today:
            raise ValidationError(
                "Stara data"
            )

    card_number = forms.CharField(validators=[card_number_validator])
    cvv = forms.CharField(validators=[cvv_validator])
    expiration_date = forms.DateField(validators=[date_validator])

    class Meta:
        model = CreditCard
        fields = ['card_number', 'expiration_date', 'card_type', 'cvv']


class PasswordGeneratorForm(forms.Form):
    choices = (
        (True, "Yes"),
        (False, "No")
    )
    upper = forms.CharField(widget=forms.Select(choices=choices))
    lower = forms.CharField(widget=forms.Select(choices=choices))
    digits = forms.CharField(widget=forms.Select(choices=choices))
    symbols = forms.CharField(widget=forms.Select(choices=choices))
    password_length = forms.IntegerField(min_value=4, max_value=48)


class PasswordCheckForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())
