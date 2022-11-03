from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import LoginData, SecretNote, CreditCard, SupportContact
from .forms import LoginDataForm, SecretNoteForm, SupportContactForm, \
    PasswordGeneratorForm, CreateUserForm, CreditCardForm, PasswordCheckForm
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from PasswordManager.PasswordHelper.password_generator import PasswordGenerator
from PasswordManager.PasswordHelper.password_check import PasswordValidator
from PasswordManager.PasswordHelper.haveibeenpwnedapi import HaveIBeenPwned
from django.core.exceptions import PermissionDenied

"""Strona Główna"""


class HomeView(View):
    def get(self, request):
        return render(request, "home.html")


"""Formularz rejestracyjny"""


class UserRegister(View):

    def get(self, request):
        form = CreateUserForm()
        context = {"form": form}
        return render(request, 'registration/register.html', context)

    def post(self, request):
        form = CreateUserForm(request.POST)
        context = {"form": form}
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect("home")
        return render(request, 'registration/register.html', context)


"""Add login data, login is required"""


class LoginDataAdd(LoginRequiredMixin, View):
    redirect_field_name = '/logindata/'

    def get(self, request):
        form = LoginDataForm()
        return render(request, "add_login_data.html", {"form": form})

    def post(self, request):
        form = LoginDataForm(request.POST)
        ctx = {"form": form}
        if form.is_valid():
            login_date = form.save(commit=False)
            login_date.user = request.user
            login_date.save()
            messages.success(request,
                             "Login data has been added successfully!")
            return redirect("all_login_data")
        return render(request, "add_login_data.html", ctx)


"""Login Data View, login is required, if user not be
 a LoginData owner raise error(PermissionDenied)"""


class LoginDataView(LoginRequiredMixin, View):
    def get(self, request, id):
        login_data = LoginData.objects.get(id=id)
        if login_data.user != request.user:
            raise PermissionDenied()
        ctx = {"login_data": login_data}
        return render(request, "login_data.html", ctx)


"""Login All Data View, login is required"""


class LoginAllDataView(LoginRequiredMixin, View):
    def get(self, request):
        login_data = LoginData.objects.filter(user=request.user)
        ctx = {"login_data": login_data}
        return render(request, "my_login_data.html", ctx)


class LoginDataEditView(LoginRequiredMixin, View):
    def get(self, request, id):
        login_data = get_object_or_404(LoginData, id=id)
        if login_data.user != request.user:
            raise PermissionDenied()
        form = LoginDataForm(instance=login_data)
        ctx = {"form": form}
        return render(request, "edit_login_data.html", ctx)

    def post(self, request, id):
        login_data = get_object_or_404(LoginData, id=id)
        form = LoginDataForm(request.POST, instance=login_data)
        ctx = {"form": form}
        if form.is_valid():
            form.save()
            return redirect("all_login_data")
        return render(request, "edit_login_data.html", ctx)


class LoginDataDeleteView(LoginRequiredMixin, View):
    def get(self, request, id):
        login_data = get_object_or_404(LoginData, id=id)
        ctx = {"login_data": login_data}
        return render(request, "delete_login_data.html", ctx)

    def post(self, request, id):
        login_data = get_object_or_404(LoginData, id=id)
        login_data.delete()
        return redirect('all_login_data')


"""Secret Note"""

"""Secret Note View"""


class SecretNoteView(LoginRequiredMixin, View):
    def get(self, request, id):
        note = SecretNote.objects.get(id=id)
        if note.user != request.user:
            raise PermissionDenied()
        ctx = {"note": note}
        return render(request, "secret_note.html", ctx)


"All user notes view"


class SecretNotesView(LoginRequiredMixin, View):
    def get(self, request):
        notes = SecretNote.objects.filter(user=request.user)
        ctx = {"notes": notes}
        return render(request, 'my_notes.html', ctx)


"""Add secret note form view"""


class SecretNoteAddView(LoginRequiredMixin, View):
    redirect_field_name = '/secret_note/'

    def get(self, request):
        form = SecretNoteForm()
        ctx = {"secret_note_form": form}
        return render(request, "add_secret_note.html", ctx)

    def post(self, request):
        form = SecretNoteForm(request.POST)
        ctx = {"secret_note_form": form}
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request,
                             "Secret Note has been added successfully!")
            return redirect("my_notes")
        return render(request, "add_secret_note.html", ctx)


"""Edit secret note View, login is required,
if auth user is not a owner raise error(permissiondenied)"""


class SecretNoteEditView(LoginRequiredMixin, View):
    def get(self, request, id):
        note = get_object_or_404(SecretNote, id=id)
        if note.user != request.user:
            raise PermissionDenied()
        form = SecretNoteForm(instance=note)
        ctx = {"form": form}
        return render(request, "edit_secret_note.html", ctx)

    def post(self, request, id):
        note = get_object_or_404(SecretNote, id=id)
        form = SecretNoteForm(request.POST, instance=note)
        ctx = {"form": form}
        if form.is_valid():
            form.save()
            return redirect('my_notes')
        return render(request, "edit_secret_note.html", ctx)


"""Delete secret note"""


class DeleteSecretNote(LoginRequiredMixin, View):
    def get(self, request, id):
        note = get_object_or_404(SecretNote, id=id)
        if note.user != request.user:
            raise PermissionDenied()
        ctx = {"note": note}
        return render(request, "delete_secret_note.html", ctx)

    def post(self, request, id):
        note = get_object_or_404(SecretNote, id=id)
        note.delete()
        return redirect('my_notes')


"""CreditCardAdd"""


class AddCreditCard(LoginRequiredMixin, View):
    def get(self, request):
        form = CreditCardForm()
        ctx = {"form": form}
        return render(request, "add_credit_card.html", ctx)

    def post(self, request):
        form = CreditCardForm(request.POST)
        ctx = {"form": form}
        if form.is_valid():
            card = form.save(commit=False)
            card.user = request.user
            card.save()
            messages.success(request,
                             "Credit Card has been added successfully!")
            return redirect('credit_cards')
        return render(request, "add_credit_card.html", ctx)


"Credit Card View, login is required, if auth user is not a data owner "


class CreditCardView(LoginRequiredMixin, View):
    def get(self, request, id):
        card = CreditCard.objects.get(id=id)
        if card.user != request.user:
            raise PermissionDenied()
        ctx = {"credit_card": card}
        return render(request, "credit_card.html", ctx)


"Credit Cards View"


class CreditCardsView(LoginRequiredMixin, View):
    def get(self, request):
        credit_cards = CreditCard.objects.filter(user=request.user)
        ctx = {"credit_cards": credit_cards}
        return render(request, 'my_credit_cards.html', ctx)


"""CreditCardsEdit"""


class CreditCardEdit(LoginRequiredMixin, View):
    def get(self, request, id):
        card = get_object_or_404(CreditCard, id=id)
        if card.user != request.user:
            raise PermissionDenied()
        form = CreditCardForm(instance=card)
        ctx = {"form": form}
        return render(request, "edit_credit_card.html", ctx)

    def post(self, request, id):
        card = get_object_or_404(CreditCard, id=id)
        form = CreditCardForm(request.POST, instance=card)
        ctx = {"form": form}
        if form.is_valid():
            form.save()
            return redirect('credit_cards')
        return render(request, "edit_credit_card.html", ctx)


"""Delete Credit Card"""


class DeleteCreditCard(LoginRequiredMixin, View):
    def get(self, request, id):
        card = get_object_or_404(CreditCard, id=id)
        if card.user != request.user:
            raise PermissionDenied()
        ctx = {"card": card}
        return render(request, "delete_credit_card.html", ctx)

    def post(self, request, id):
        card = get_object_or_404(CreditCard, id=id)
        card.delete()
        return redirect('credit_cards')


"""Formularz kontaktowy"""


class SupportContactView(View):
    def get(self, request):
        form = SupportContactForm()
        ctx = {"support_contact_form": form}
        return render(request, "support_contact.html", ctx)

    def post(self, request):
        form = SupportContactForm(request.POST)
        ctx = {"support_contact_form": form}
        if form.is_valid():
            form.save()
            return redirect('home')
        return render(request, "support_contact.html", ctx)


"""Wszystkie zgłoszenia"""


class SupportCases(PermissionRequiredMixin, View):
    permission_required = 'is_staff'

    def get(self, request):
        all_support_cases = SupportContact.objects.all()
        ctx = {"all_support_cases": all_support_cases}
        return render(request, "support_cases.html", ctx)


"""Pojedyńcze zgłoszenie"""


class SupportCase(PermissionRequiredMixin, View):
    permission_required = "is_staff"

    def get(self, request, id):
        case = get_object_or_404(SupportContact, id=id)
        ctx = {"case": case}
        return render(request, "support_case.html", ctx)


class PasswordGeneratorView(View, PasswordGenerator):

    def get(self, request):
        form = PasswordGeneratorForm()
        ctx = {"password_generator_form": form}
        return render(request, "password_generator.html", ctx)

    def post(self, request):
        form = PasswordGeneratorForm(request.POST)
        ctx = {"password_generator_form": form}

        if form.is_valid():
            upper = form.cleaned_data["upper"]
            lower = form.cleaned_data["lower"]
            digits = form.cleaned_data["digits"]
            symbols = form.cleaned_data["symbols"]
            password_length = form.cleaned_data["password_length"]
            new_password = PasswordGenerator(password_length, upper,
                                             lower, digits, symbols)
            ctx['new_password'] = str(new_password.password_generate())
            return render(request, "password_generator.html", ctx)


class PasswordCheckView(View, PasswordValidator):
    def get(self, request):
        form = PasswordCheckForm()
        ctx = {"form": form}
        return render(request, "password_check.html", ctx)

    def post(self, request):
        form = PasswordCheckForm(request.POST)
        ctx = {"form": form}
        if form.is_valid():
            password = form.cleaned_data['password']
            password_check = PasswordValidator(password)
            ctx['checked_password'] = str(password_check.password_validation())
            ctx['password_seen'] = str(
                password_check.password_seen_in_data_branch())
            return render(request, 'password_check.html', ctx)


class HaveIBeenPwnedView(LoginRequiredMixin, View, HaveIBeenPwned):
    def get(self, request):
        emails = LoginData.objects.filter(user=request.user).values('email')
        emails_list = []
        pwned_list = []
        for email in emails:
            if email['email'] not in emails_list:
                emails_list.append(email['email'])
        ctx = {"emails": emails_list, 'pwned_list': pwned_list}
        for email in emails_list:
            pwned_email = HaveIBeenPwned(email)
            pwned_list.append(f"Your mail address: {email} {pwned_email.get_pwned_info()}")
        return render(request, "have_i_been_pwned.html", ctx)
