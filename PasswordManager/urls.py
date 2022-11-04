from django.contrib import admin
from django.urls import path, include
from password_manager_app.views import LoginDataAdd, SecretNoteAddView, SupportContactView, \
    PasswordGeneratorView, HomeView, UserRegister, SecretNotesView, SecretNoteView, SecretNoteEditView, \
    DeleteSecretNote, AddCreditCard, CreditCardView, CreditCardsView, CreditCardEdit, DeleteCreditCard, \
    LoginDataView, LoginAllDataView, PasswordCheckView, LoginDataEditView, LoginDataDeleteView, HaveIBeenPwnedView, \
    SupportCases, SupportCase, SupportCaseDelete, AboutUs

urlpatterns = [
    path('admin/', admin.site.urls),
    path('support_contact/', SupportContactView.as_view(), name="support_contact"),
    path('password_generator/', PasswordGeneratorView.as_view(), name="password_generator"),
    path('home/', HomeView.as_view(), name="home"),
    path('', include('django.contrib.auth.urls')),
    path('register/', UserRegister.as_view(), name="register"),
    path('secret_note_add/', SecretNoteAddView.as_view(), name="secret_note_add"),
    path('secret_note/<int:id>', SecretNoteView.as_view(), name="secret_note"),
    path('notes/', SecretNotesView.as_view(), name="my_notes"),
    path('edit_secret_note/<int:id>', SecretNoteEditView.as_view(), name="edit_secret_note"),
    path('delete_secret_note/<int:id>', DeleteSecretNote.as_view(), name="delete_secret_note"),
    path('add_credit_card/', AddCreditCard.as_view(), name="add_credit_card"),
    path('credit_card/<int:id>', CreditCardView.as_view(), name="credit_card"),
    path('credit_cards/', CreditCardsView.as_view(), name='credit_cards'),
    path('edit_credit_card/<int:id>', CreditCardEdit.as_view(), name="edit_credit_card"),
    path('delete_credit_card/<int:id>', DeleteCreditCard.as_view(), name="delete_credit_card"),
    path('add_login_data/', LoginDataAdd.as_view(), name="add_login_data"),
    path('login_data/<int:id>', LoginDataView.as_view(), name="login_data"),
    path('all_login_data/', LoginAllDataView.as_view(), name="all_login_data"),
    path('password_check', PasswordCheckView.as_view(), name="password_check"),
    path('edit_login_data/<int:id>', LoginDataEditView.as_view(), name="edit_login_data"),
    path('delete_login_data/<int:id>', LoginDataDeleteView.as_view(), name="delete_login_data"),
    path('have_i_been_pwned/', HaveIBeenPwnedView.as_view(), name="have_i_been_pwned"),
    path('support_cases/', SupportCases.as_view(), name="support_cases"),
    path('support_case/<int:id>', SupportCase.as_view(), name="support_case"),
    path('delete_support_case/<int:id>', SupportCaseDelete.as_view(), name="delete_support_case"),
    path('about_us', AboutUs.as_view(), name="about_us")
]
