from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.views import View
from .models import User, UserActivity
from django.utils.crypto import get_random_string
from django.http import Http404, HttpRequest
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from account_module.forms import RegisterForm, LoginForm, ForgetPassForm, ResetForm
from django.core.mail import send_mail


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        context = {
            'register_form': register_form
        }

        return render(request, 'account_module/register.html', context)

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_email = register_form.cleaned_data.get('email')
            user_password = register_form.cleaned_data.get('password')
            name = register_form.cleaned_data.get('name')
            family = register_form.cleaned_data.get('family')
            user: bool = User.objects.filter(email__iexact=user_email).exists()
            if user:
                register_form.add_error('email', 'ایمیل وارد شده تکراری می باشد')
            else:
                new_user = User(
                    email=user_email,
                    email_active_code=get_random_string(72),
                    is_active=False,
                    username=user_email,
                    first_name=name,
                    last_name=family,
                )
                new_user.set_password(user_password)
                new_user.save()
                user_activity = UserActivity(
                    user=new_user,
                    name=new_user.get_full_name(),
                    date_joined=new_user.date_joined,
                )
                url = f'http://localhost:8000/activate-account/{new_user.email_active_code}'
                user_activity.save()
                send_mail(
                    subject='welcome',
                    message='This is a plain text fallback message.',
                    from_email='dvd8304@gmail.com',
                    recipient_list=[user_email],
                    fail_silently=False,
                    html_message=f'''
                                    <!DOCTYPE html>
                                    <html>
                                    <body>
                                    <h2>تایید حساب</h2>
                                    <p>برای تایید حساب بر روی لینک زیر کلیک کنید</p>
                                    <a href=http://localhost:8000/activate-account/{new_user.email_active_code}>کلیک کنید</a>
                                    </body>
                                    </html>
                                '''
                )
                return redirect(reverse('login_page'))

        context = {
            'register_form': register_form
        }

        return render(request, 'account_module/register.html', context)


class ActivateAccountView(View):
    def get(self, request, email_active_code):
        user: User = User.objects.filter(email_active_code__iexact=email_active_code).first()
        if user is not None:
            if not user.is_active:
                user.is_active = True
                user.email_active_code = get_random_string(72)
                user.save()
                return redirect(reverse('login_page'))
            else:
                pass

        raise Http404


class LoginView(View):
    def get(self, request):
        if request.session.session_key:
            return redirect(reverse('weather'))
        login_form = LoginForm()
        context = {
            'login_form': login_form
        }

        return render(request, 'account_module/login.html', context)

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_email = login_form.cleaned_data.get('email')
            user_pass = login_form.cleaned_data.get('password')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                if not user.is_active:
                    login_form.add_error('email', 'حساب کاربری شما فعال نشده است')
                else:
                    is_password_correct = user.check_password(user_pass)
                    if is_password_correct:
                        login(request, user)
                        print("test")
                        return redirect(reverse('weather'))
                    else:
                        login_form.add_error('email', 'کلمه عبور اشتباه است')
            else:
                login_form.add_error('email', 'کاربری با مشخصات وارد شده یافت نشد')

        context = {
            'login_form': login_form
        }

        return render(request, 'account_module/login.html', context)


class logoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('login_page'))


class ForgetPassword(View):
    def get(self, request: HttpRequest):
        forget_pass_form = ForgetPassForm()
        context = {'forget_pass_form': forget_pass_form}
        return render(request, 'account_module/ForgetPassword.html', context)

    def post(self, request: HttpRequest):
        forget_pass_form = ForgetPassForm(request.POST)
        if forget_pass_form.is_valid():
            user_email = forget_pass_form.cleaned_data.get('email')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                pass

        context = {'forget_pass_form': forget_pass_form}
        return render(request, 'account_module/ForgetPassword.html', context)


class ResetPassword(View):
    def get(self, request: HttpRequest, active_code):
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if user is None:
            return redirect(reverse('login_page'))

        reset_pass_form = ResetForm()
        context = {
            'reset_pass_form': reset_pass_form,
            'user': user
        }
        return render(request, 'account_module/ResetPass.html', context)

    def post(self, request: HttpRequest, active_code):
        reset_pass_form = ResetForm(request.POST)
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if reset_pass_form.is_valid():
            if user is None:
                return redirect(reverse('login_page'))
            user_new_pass = reset_pass_form.cleaned_data.get('password')
            user.set_password(user_new_pass)
            user.email_active_code = get_random_string(72)
            user.is_active = True
            user.save()
            return redirect(reverse('login_page'))

        context = {
            'reset_pass_form': reset_pass_form,
            'user': user
        }
        return render(request, 'account_module/ResetPass.html', context)
