from django import forms
from django.core import validators
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox


class RegisterForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        min_length=3,
        label='نام',
        widget=forms.TextInput(),
        error_messages={'required': 'لطفا نام خود را وارد نمایید'},
    )
    family = forms.CharField(
        max_length=100,
        min_length=3,
        label='نام خانوادگی',
        widget=forms.TextInput(),
        error_messages={'required': 'لطفا نام خانوادگی خود را وارد نمایید'},
    )
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator,
        ]
    )
    password = forms.CharField(
        label='کلمه عبور',
        widget=forms.PasswordInput(),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    confirm_password = forms.CharField(
        label='تکرار کلمه عبور',
        widget=forms.PasswordInput(),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    # def clean_confirm_password(self):
    #     password = self.cleaned_data.get('password')
    #     confirm_password = self.cleaned_data.get('confirm_password')
    #
    #     if password == confirm_password:
    #         return confirm_password
    #
    #     raise ValidationError('کلمه عبور و تکرار کلمه عبور مغایرت دارند')
    #
    # def clean(self):
    #     cleaned_data = super(RegisterForm, self).clean()
    #     password = cleaned_data.get('password')
    #
    #     min_length = 8
    #     if len(password) < min_length:
    #         msg = 'رمز عبور باید حداقل 8 کاراکتر باشد.'
    #         self.add_error('password', msg)
    #
    #     if sum(c.isdigit() for c in password) < 1:
    #         msg = 'رمز عبور باید حداقل شامل یک رقم باشد.'
    #         self.add_error('password', msg)
    #
    #     if not any(c.isupper() for c in password):
    #         msg = 'رمز عبور باید حداقل شامل یک حرف بزرگ انگلیسی باشد.'
    #         self.add_error('password', msg)
    #
    #     if not any(c.islower() for c in password):
    #         msg = 'رمز عبور باید حداقل شامل یک حرف کوچک انگلیسی باشد.'
    #         self.add_error('password', msg)
    #
    #     password_confirm = cleaned_data.get('password2')
    #
    #     if password and password_confirm:
    #         if password != password_confirm:
    #             msg = "The two password fields must match."
    #             self.add_error('password_confirm', msg)
    #     return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator
        ]
    )
    password = forms.CharField(
        label='کلمه عبور',
        widget=forms.PasswordInput(),
        validators=[
            validators.MaxLengthValidator(100)
        ]
    )
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox(
            attrs={'data-theme': 'light'}
        )
    )


class ForgetPassForm(forms.Form):
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator
        ]
    )


class ResetForm(forms.Form):
    password = forms.CharField(
        label='کلمه عبور',
        widget=forms.PasswordInput(),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    confirm_password = forms.CharField(
        label='تکرار کلمه عبور',
        widget=forms.PasswordInput(),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    # def clean_confirm_password(self):
    #     password = self.cleaned_data.get('password')
    #     confirm_password = self.cleaned_data.get('confirm_password')
    #
    #     if password == confirm_password:
    #         return confirm_password
    #
    #     raise ValidationError('کلمه عبور و تکرار کلمه عبور مغایرت دارند')
    #
    # def clean(self):
    #     cleaned_data = super(ResetForm, self).clean()
    #     password = cleaned_data.get('password')
    #
    #     min_length = 8
    #     if len(password) < min_length:
    #         msg = 'رمز عبور باید حداقل 8 کاراکتر باشد.'
    #         self.add_error('password', msg)
    #
    #     if sum(c.isdigit() for c in password) < 1:
    #         msg = 'رمز عبور باید حداقل شامل یک رقم باشد.'
    #         self.add_error('password', msg)
    #
    #     if not any(c.isupper() for c in password):
    #         msg = 'رمز عبور باید حداقل شامل یک حرف بزرگ انگلیسی باشد.'
    #         self.add_error('password', msg)
    #
    #     if not any(c.islower() for c in password):
    #         msg = 'رمز عبور باید حداقل شامل یک حرف کوچک انگلیسی باشد.'
    #         self.add_error('password', msg)
    #
    #     password_confirm = cleaned_data.get('password2')
    #
    #     if password and password_confirm:
    #         if password != password_confirm:
    #             msg = "The two password fields must match."
    #             self.add_error('password_confirm', msg)
    #     return cleaned_data