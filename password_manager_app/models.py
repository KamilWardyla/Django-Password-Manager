from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models
from encrypted_model_fields.fields import EncryptedCharField, \
    EncryptedTextField

CARD_TYPES = (
    ("Visa", "Visa"),
    ("MasterCard", "MasterCard"),
    ("AmericanExpress", "AmericanExpress"),
    ("Discover", "Discover"),
)
LOGIN_DATA_TYPES = (
    ("Web Application Password", "Web Application Password"),
    ("Mail Account", "Mail Account"),
    ("Online Identies", "Online Identies"),
    ("Social Media", "Social Media"),
    ("Financial Record", "Financial Record"),
    ("Desktop App", "Desktop App"),
    ("Mobie App", "Mobie App"),
)


class User(AbstractUser):
    username = models.CharField(max_length=32, unique=True,
                                help_text="Required. 32 characters or fewer. Letters, digits and @/./+/-/_ only.",
                                error_messages={
                                    "unique": _("A user with that username already exists."),
                                })
    email = models.EmailField(unique=True, blank=False)
    is_staff = models.BooleanField(_("staff status"), default=False,
                                   help_text=_("Designates whether the user can log into this admin site."))
    is_active = models.BooleanField(_("active"), default=True, help_text=_(
        "Designates whether this user should be treated as active. "
        "Unselect this instead of deleting accounts."
    ), )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "password"]


class SecretNote(models.Model):
    note_name = models.CharField(max_length=32, null=False)
    note_text = EncryptedTextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.note_name

    class Meta:
        ordering = ['note_name']


class LoginData(models.Model):
    data_name = models.CharField(null=False, max_length=32)
    login_name = models.CharField(null=False, max_length=64)
    email = models.EmailField(blank=True)
    password = EncryptedCharField(max_length=30)
    url = models.CharField(max_length=64, blank=True)
    login_data_group = models.CharField(choices=LOGIN_DATA_TYPES, max_length=32)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.data_name

    class Meta:
        ordering = ['data_name']


class CreditCard(models.Model):
    card_number = models.CharField(max_length=16, unique=True)
    expiration_date = models.DateField()
    card_type = models.CharField(choices=CARD_TYPES, max_length=32)
    cvv = EncryptedCharField(max_length=3)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.card_type


class SupportContact(models.Model):
    topic = models.CharField(max_length=128)
    sender_email = models.EmailField(blank=False)
    message_text = models.TextField(blank=False)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.topic

    class Meta:
        ordering = ['creation_date']
