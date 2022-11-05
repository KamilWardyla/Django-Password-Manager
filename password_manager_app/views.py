from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import LoginData, SecretNote, CreditCard, SupportContact
from .forms import LoginDataForm, SecretNoteForm, SupportContactForm, \
    PasswordGeneratorForm, CreateUserForm, CreditCardForm, PasswordCheckForm
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from PasswordManager.PasswordHelper.password_generator import PasswordGenerator
from PasswordManager.PasswordHelper.password_check import PasswordValidator
from PasswordManager.PasswordHelper.haveibeenpwnedapi import HaveIBeenPwned
from django.core.exceptions import PermissionDenied


class HomeView(View):
    def get(self, request):
        return render(request, "home.html")


class UserRegister(View):
    """This class is for register the user."""

    def get(self, request):
        """Return the view contains form to create user.
                    Parameters:
                    request -- argument contains request from browser
                        """
        if request.user.is_authenticated:
            messages.warning(request,
                             "You are already logged-in, if you want to register another account logout first")
            return redirect('home')
        form = CreateUserForm()
        context = {"form": form}
        return render(request, 'registration/register.html', context)

    def post(self, request):
        """" Check crate user form correctness, save form, login user and redirect page to 'home' if form is valid
                        or render 'registration/register.html' template
                        Parameters:
                           request -- argument contains request from browser
                        """
        form = CreateUserForm(request.POST)
        context = {"form": form}
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect("home")
        return render(request, 'registration/register.html', context)


class LoginDataAdd(LoginRequiredMixin, View):
    redirect_field_name = '/logindata/'
    """This class is for adding the login data."""

    def get(self, request):
        """Return the view contains form to add login data.
            Parameters:
            request -- argument contains request from browser
                """
        form = LoginDataForm()
        return render(request, "add_login_data.html", {"form": form})

    def post(self, request):
        """" Check login form correctness, save login data and redirect page to 'all_login_data' if form is valid
                or render 'add_login_data.html' template
                Parameters:
                   request -- argument contains request from browser
                """
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


class LoginDataView(LoginRequiredMixin, View):
    """This class displays the user login data"""

    def get(self, request, id):
        """Check the login_data.user is equal to logged-in user if is equal :return the view 'login data.html',
        if it's not raise PermissionDenied
                   Parameters
                   request -- argument contains request from browser
                   id -- argument contains LoginData.id
                       """
        login_data = LoginData.objects.get(id=id)
        if login_data.user != request.user:
            raise PermissionDenied()
        ctx = {"login_data": login_data}
        return render(request, "login_data.html", ctx)


class LoginAllDataView(LoginRequiredMixin, View):
    """This class displays the user all  login data"""

    def get(self, request):
        """Get the user login data and return the view 'my_login_data.html'
                           Parameters
                           request -- argument contains request from browser
                               """

        login_data = LoginData.objects.filter(user=request.user)
        ctx = {"login_data": login_data}
        return render(request, "my_login_data.html", ctx)


class LoginDataEditView(LoginRequiredMixin, View):
    """This class is for editing the login data."""

    def get(self, request, id):
        """Return the view contains form to edit login data.
                    Parameters:
                    request -- argument contains request from browser
                    id -- argument contains LoginData.id
                        """
        login_data = get_object_or_404(LoginData, id=id)
        if login_data.user != request.user:
            raise PermissionDenied()
        form = LoginDataForm(instance=login_data)
        ctx = {"form": form}
        return render(request, "edit_login_data.html", ctx)

    def post(self, request, id):
        """" Check login form correctness, save login data and redirect page to 'all_login_data' if form is valid
                        or render 'edit_login_data.html' template
                        Parameters:
                           request -- argument contains request from browser
                           id -- argument contains LoginData.id
                        """
        login_data = get_object_or_404(LoginData, id=id)
        if login_data.user != request.user:
            raise PermissionDenied()
        form = LoginDataForm(request.POST, instance=login_data)
        ctx = {"form": form}
        if form.is_valid():
            form.save()
            return redirect("all_login_data")
        return render(request, "edit_login_data.html", ctx)


class LoginDataDeleteView(LoginRequiredMixin, View):
    """This class is for deleting the login data."""

    def get(self, request, id):
        """Check the login_data.user is equal to logged-in user if is equal :return the view 'delete_login_data.html',
               if it's not raise PermissionDenied
                          Parameters
                          request -- argument contains request from browser
                          id -- argument contains LoginData.id
                              """
        login_data = get_object_or_404(LoginData, id=id)
        if login_data.user != request.user:
            raise PermissionDenied()
        ctx = {"login_data": login_data}
        return render(request, "delete_login_data.html", ctx)

    def post(self, request, id):
        """" Delete login data and redirect to 'all_login_data'
                                Parameters:
                                   request -- argument contains request from browser
                                   id -- argument contains LoginData.id
                                """
        login_data = get_object_or_404(LoginData, id=id)
        login_data.delete()
        return redirect('all_login_data')


"""Secret Note"""


class SecretNoteAddView(LoginRequiredMixin, View):
    """This class is for adding the secret note."""

    redirect_field_name = '/secret_note/'

    def get(self, request):
        """Return the view contains form to add secret note.
                    Parameters:
                    request -- argument contains request from browser
                        """
        form = SecretNoteForm()
        ctx = {"secret_note_form": form}
        return render(request, "add_secret_note.html", ctx)

    def post(self, request):
        """" Check secret note form correctness, save secret note and redirect page to 'my_notes' if form is valid
                        or render 'add_secret_note.html' template
                        Parameters:
                           request -- argument contains request from browser
                        """
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


class SecretNoteView(LoginRequiredMixin, View):
    """This class displays the user secret note"""

    def get(self, request, id):
        """Check the secret note owner is equal to logged-in user if is equal :return the view 'secret_note.html',
        if it's not raise PermissionDenied
                   Parameters
                   request -- argument contains request from browser
                   id -- argument contains SecretNote.id
                       """
        note = SecretNote.objects.get(id=id)
        if note.user != request.user:
            raise PermissionDenied()
        ctx = {"note": note}
        return render(request, "secret_note.html", ctx)


class SecretNotesView(LoginRequiredMixin, View):
    """This class displays the user all secret notes"""

    def get(self, request):
        """Get the user secret notes and return the view 'my_notes.html'
                                           Parameters
                                           request -- argument contains request from browser
                                               """
        notes = SecretNote.objects.filter(user=request.user)
        ctx = {"notes": notes}
        return render(request, 'my_notes.html', ctx)


class SecretNoteEditView(LoginRequiredMixin, View):
    """This class is for editing the secret note."""

    def get(self, request, id):
        """Return the view contains form to edit login data.
                            Parameters:
                            request -- argument contains request from browser
                            id -- argument contains SecretNote.id
                                """
        note = get_object_or_404(SecretNote, id=id)
        if note.user != request.user:
            raise PermissionDenied()
        form = SecretNoteForm(instance=note)
        ctx = {"form": form}
        return render(request, "edit_secret_note.html", ctx)

    def post(self, request, id):
        """ Check secret note form correctness, save secret note and redirect page to 'my_notes' if form is valid
                                or render 'edit_login_data.html' template
                                Parameters:
                                   request -- argument contains request from browser
                                   id -- argument contains SecretNote.id
                                """
        note = get_object_or_404(SecretNote, id=id)
        form = SecretNoteForm(request.POST, instance=note)
        ctx = {"form": form}
        if form.is_valid():
            form.save()
            return redirect('my_notes')
        return render(request, "edit_secret_note.html", ctx)


class DeleteSecretNote(LoginRequiredMixin, View):
    """This class is for deleting the secret note."""

    def get(self, request, id):
        """Check the secret note owner is equal to logged-in user if is equal :return the view 'delete_secret_note.html',
                       if it's not raise PermissionDenied
                                  Parameters
                                  request -- argument contains request from browser
                                  id -- argument contains SecretNote.id
                                      """
        note = get_object_or_404(SecretNote, id=id)
        if note.user != request.user:
            raise PermissionDenied()
        ctx = {"note": note}
        return render(request, "delete_secret_note.html", ctx)

    def post(self, request, id):
        """" Delete secret_note and redirect to 'my_notes'
                                        Parameters:
                                           request -- argument contains request from browser
                                           id -- argument contains SecretNote.id
                                        """
        note = get_object_or_404(SecretNote, id=id)
        note.delete()
        return redirect('my_notes')


"""CreditCard"""


class AddCreditCard(LoginRequiredMixin, View):
    """This class is for adding the credit card."""

    def get(self, request):
        """Return the view contains form to add credit card.
                            Parameters:
                            request -- argument contains request from browser
                                """
        form = CreditCardForm()
        ctx = {"form": form}
        return render(request, "add_credit_card.html", ctx)

    def post(self, request):
        """" Check credit card form correctness, save credit card and redirect page to 'credit_cards' if form is valid
                                or render 'add_credit_card.html' template
                                Parameters:
                                   request -- argument contains request from browser
                                """
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


class CreditCardView(LoginRequiredMixin, View):
    """This class displays the user credit card"""

    def get(self, request, id):
        """Check the credit card data owner is equal to logged-in user if is equal :return the view 'credit_card.html',
               if it's not raise PermissionDenied
                          Parameters
                          request -- argument contains request from browser
                          id -- argument contains CreditCard.id
                              """
        card = CreditCard.objects.get(id=id)
        if card.user != request.user:
            raise PermissionDenied()
        ctx = {"credit_card": card}
        return render(request, "credit_card.html", ctx)


class CreditCardsView(LoginRequiredMixin, View):
    """This class displays the user all credit cards"""

    def get(self, request):
        """Get the user credit cards data and return the 'my_credit_cards.html' template
                                                   Parameters
                                                   request -- argument contains request from browser
                                                       """
        credit_cards = CreditCard.objects.filter(user=request.user)
        ctx = {"credit_cards": credit_cards}
        return render(request, 'my_credit_cards.html', ctx)


class CreditCardEdit(LoginRequiredMixin, View):
    """This class is for editing the credit card data."""

    def get(self, request, id):
        """Return the view contains form to edit credit card data.
                                    Parameters:
                                    request -- argument contains request from browser
                                    id -- argument contains CreditCard.id
                                        """
        card = get_object_or_404(CreditCard, id=id)
        if card.user != request.user:
            raise PermissionDenied()
        form = CreditCardForm(instance=card)
        ctx = {"form": form}
        return render(request, "edit_credit_card.html", ctx)

    def post(self, request, id):
        """ Check credit card form correctness, save credit card and redirect page to 'credit_cards' if form is valid
                                        or render 'edit_credit_card.html' template
                                        Parameters:
                                           request -- argument contains request from browser
                                           id -- argument contains CreditCard.id
                                        """
        card = get_object_or_404(CreditCard, id=id)
        form = CreditCardForm(request.POST, instance=card)
        ctx = {"form": form}
        if form.is_valid():
            form.save()
            return redirect('credit_cards')
        return render(request, "edit_credit_card.html", ctx)


class DeleteCreditCard(LoginRequiredMixin, View):
    """This class is for deleting the credit card data."""

    def get(self, request, id):
        """Check the credit card owner is equal to logged-in user if is equal :return the view 'delete_credit_card.html',
                               if it's not raise PermissionDenied
                                          Parameters:
                                          request -- argument contains request from browser
                                          id -- argument contains CreditCard.id
                                              """
        card = get_object_or_404(CreditCard, id=id)
        if card.user != request.user:
            raise PermissionDenied()
        ctx = {"card": card}
        return render(request, "delete_credit_card.html", ctx)

    def post(self, request, id):
        """" Delete credit card data and redirect to 'credit_cards'
                Parameters:
                          request -- argument contains request from browser
                          id -- argument contains CreditCard.id
                                            """
        card = get_object_or_404(CreditCard, id=id)
        card.delete()
        return redirect('credit_cards')


"""Formularz kontaktowy"""


class SupportContactView(View):
    """This class is for creating the support case."""

    def get(self, request):
        """Return the view contains form to create support case.
                            Parameters:
                            request -- argument contains request from browser
                                """
        form = SupportContactForm()
        ctx = {"support_contact_form": form}
        return render(request, "support_contact.html", ctx)

    def post(self, request):
        """ Check support contact form correctness, save support case and redirect page to 'home' if form is valid
                                or render 'support_contact.html.html' template
                                Parameters:
                                   request -- argument contains request from browser
                                """
        form = SupportContactForm(request.POST)
        ctx = {"support_contact_form": form}
        if form.is_valid():
            form.save()
            return redirect('home')
        return render(request, "support_contact.html", ctx)


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """This class is for creating StaffRequiredMixin"""

    def test_func(self):
        """This method check if request.user.is_staff is equal True if not deny request with permission error"""
        return self.request.user.is_staff


class SupportCases(StaffRequiredMixin, View):
    """This class displays all support cases"""

    def get(self, request):
        """Get the support cases and return the "support_cases.html" template if user.is_staff
                        Parameters
                        request -- argument contains request from browser
                                                                       """
        all_support_cases = SupportContact.objects.all()
        ctx = {"all_support_cases": all_support_cases}
        return render(request, "support_cases.html", ctx)


class SupportCase(StaffRequiredMixin, View):
    """This class displays the support case"""

    def get(self, request, id):
        """Return the view 'support_case.html when logged-in user is staff,
                                  Parameters
                                  request -- argument contains request from browser
                                  id -- argument contains SupportContact.id
                                      """
        case = get_object_or_404(SupportContact, id=id)
        ctx = {"case": case}
        return render(request, "support_case.html", ctx)


class SupportCaseDelete(StaffRequiredMixin, View):
    """This class is for deleting the support case."""

    def get(self, request, id):
        """Return the view "delete_support_case.html" when logged-in user is staff
        Parameters
                request -- argument contains request from browser
                id -- argument contains SupportContact.id"""

        case = get_object_or_404(SupportContact, id=id)
        ctx = {"case": case}
        return render(request, "delete_support_case.html", ctx)

    def post(self, request, id):
        """" Delete support case and redirect to 'support_cases'
                        Parameters:
                                  request -- argument contains request from browser
                                  id -- argument contains SupportContact.id
                                                    """
        case = get_object_or_404(SupportContact, id=id)
        case.delete()
        return redirect('support_cases')


class PasswordGeneratorView(View, PasswordGenerator):
    """This class is for generating password."""

    def get(self, request):
        """Return the view contains form to generating password.
                            Parameters:
                            request -- argument contains request from browser
                                """
        form = PasswordGeneratorForm()
        ctx = {"password_generator_form": form}
        return render(request, "password_generator.html", ctx)

    def post(self, request):
        """ Check password generator form correctness, puts the generated password into the context and render
        'password_generator.html' template.
                                Parameters:
                                   request -- argument contains request from browser
                                """
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
    """This class is for check your password."""

    def get(self, request):
        """Return the view contains form to check password.
                            Parameters:
                            request -- argument contains request from browser
                                """
        form = PasswordCheckForm()
        ctx = {"form": form}
        return render(request, "password_check.html", ctx)

    def post(self, request):
        """ Check password check form correctness, puts the checked password and password_seen into the context and render
                'password_check.html' template.
                                        Parameters:
                                           request -- argument contains request from browser
                                        """
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
    """This class is for check your email has been pwned."""

    def get(self, request):
        emails = LoginData.objects.filter(user=request.user).values('email')
        emails_list = []
        pwned_list = []
        for email in emails:
            if len(email['email']) == 0:
                pass
            elif email['email'] not in emails_list:
                emails_list.append(email['email'])
        ctx = {"emails": emails_list, 'pwned_list': pwned_list}
        for email in emails_list:
            pwned_email = HaveIBeenPwned(email)
            pwned_list.append(f"Your mail address: {email} {pwned_email.get_pwned_info()}")
        return render(request, "have_i_been_pwned.html", ctx)


class AboutUs(View):
    """This class is for render about_us template"""

    def get(self, request):
        return render(request, "about_us.html")
