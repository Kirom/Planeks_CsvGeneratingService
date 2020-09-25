from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, \
    PasswordResetCompleteView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.shortcuts import render, redirect, resolve_url

from django.template.loader import render_to_string

from django.utils.encoding import force_bytes, force_text
from django.utils.http import url_has_allowed_host_and_scheme, urlsafe_base64_encode, urlsafe_base64_decode

from .forms import UserLoginForm, UserRegistrationForm
from .tokens import account_activation_token


def home(request):
    return render(request, 'accounts/home.html')


def login_view(request):
    form = UserLoginForm(request.POST or None)
    next_ = request.GET.get('next')
    if form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username.strip(), password=password.strip())
        login(request, user)
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or '/'
        return redirect(redirect_path)
    return render(request, 'accounts/home.html', context={'form': form, })


# class UserLoginView(LoginView):
#     template_name = 'login.html'
#     redirect_authenticated_user = True
#     # authentication_form = UserLoginForm()
#
#     def get_form_class(self):
#         return UserLoginForm(self.request.POST or None)
#
#     def get_redirect_url(self):
#         """Return the user-originating redirect URL if it's safe."""
#         redirect_to = self.request.POST.get(
#             self.redirect_field_name,
#             self.request.GET.get(self.redirect_field_name, '/')
#         )
#         url_is_safe = url_has_allowed_host_and_scheme(
#             url=redirect_to,
#             allowed_hosts=self.get_success_url_allowed_hosts(),
#             require_https=self.request.is_secure(),
#         )
#         return redirect_to if url_is_safe else '/'


def logout_view(request):
    logout(request)
    return redirect('fakecsv:data_schema_list')


def registration_view(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.is_active = False
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            current_site = get_current_site(request)
            mail_subject = f'Активация аккаунта на {current_site}'
            message = render_to_string('accounts/acc_activation_email.html', {
                'user': new_user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                'token': account_activation_token.make_token(new_user),
            })
            to_email = user_form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()

            return render(request, 'accounts/registration_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'accounts/registration.html', {'form': user_form})


def activate_account(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        return render(request, 'accounts/acc_activation_done.html', {'username': user})
    else:
        return render(request, 'accounts/acc_activation_failed.html')


class UserPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    success_url = 'done/'
    email_template_name = 'accounts/password_reset_email.html'


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = 'reset/done/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.get_user(self.kwargs.get('uidb64'))
        context['username'] = username
        return context


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
# class RegistrationView(FormView):
#     form_class = UserRegistrationForm
#     success_url = "/login/"
#     template_name = 'registration.html'
#
#     def form_valid(self, form):
#         form.save()
#         # Функция super( тип [ , объект или тип ] )
#         # Возвратите объект прокси, который делегирует вызовы метода родительскому или родственному классу типа .
#         return super(RegistrationView, self).form_valid(form)
#
#     def form_invalid(self, form):
#         return super(RegistrationView, self).form_invalid(form)
