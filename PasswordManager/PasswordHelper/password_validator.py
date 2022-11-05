from django.core.exceptions import ValidationError
from django.utils.translation import gettext as e
from django.contrib.auth.password_validation import UserAttributeSimilarityValidator

UPPER_CASE_LETTER = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                     'S', 'T', 'U', 'V', 'W', 'X', 'Y']
LOWER_CASE_LETTER = list(map(lambda letter: letter.lower(), UPPER_CASE_LETTER))
DIGITS = [str(x) for x in range(0, 10)]
SYMBOLS = ['`', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '-', '=', '{', '}', '[', ']', ':',
           ';', '|', '\\', '<', '>', '?', ',', '.', '/', '`', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_',
           '+', '-', '=', '{', '}', '[', ']', ':', ';', '|', '<', '>', '?', ',', '.', '/']


class MyMinimumLengthValidator:
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError(
                e(f"This password must contain at least {8} characters."),
                code="password_too_short")

    def get_help_text(self):
        return e(f"Your password must contain at least {8} characters.")


class UpperCaseCharacterValidator:
    global UPPER_CASE_LETTER

    def validate(self, password, user=None):
        if not any([i for i in password if i in UPPER_CASE_LETTER]):
            raise ValidationError(
                e(f"This password must contain at least one uppercase character"),
                code="password_without_uppercase"
            )

    def get_help_text(self):
        return e(f"Your password must contain at least one uppercase character")


class LowerCaseCharacterValidator:
    global LOWER_CASE_LETTER

    def validate(self, password, user=None):
        if not any([i for i in password if i not in LOWER_CASE_LETTER]):
            raise ValidationError(
                e(f"This password must contain at least one lowercase character"),
                code="password_without_uppercase"
            )

    def get_help_text(self):
        return e(f"Your password must contain at least one uppercase character")


class DigitsCharacterValidator:
    global DIGITS

    def validate(self, password, user=None):
        if not any([i for i in password if i in DIGITS]):
            raise ValidationError(
                e(f"This password must contain at least one digit character"),
                code="password_without_uppercase"
            )

    def get_help_text(self):
        return e(f"Your password must contain at least one digit character")


class SymbolCharacterValidator:
    global SYMBOLS

    def validate(self, password, user=None):
        if not any([i for i in password if i in SYMBOLS]):
            raise ValidationError(
                e(f"This password must contain at least one symbol character"),
                code="password_without_uppercase"
            )

    def get_help_text(self):
        return e(f"Your password must contain at least one symbol character")


class MyUserAttributeSimilarityValidator(UserAttributeSimilarityValidator):
    DEFAULT_USER_ATTRIBUTES = ("username", "email")

    def __init__(self, user_attributes=DEFAULT_USER_ATTRIBUTES, max_similarity=0.6):
        super().__init__(user_attributes=self.DEFAULT_USER_ATTRIBUTES, max_similarity=0.6)
        self.user_attributes = user_attributes
        if max_similarity < 0.1:
            raise ValueError("max_similarity must be at least 0.1")
        self.max_similarity = max_similarity
