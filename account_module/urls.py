from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register_page'),
    path('', views.LoginView.as_view(), name='login_page'),
    path('forget_pass', views.ForgetPassword.as_view(), name='forget_password_page'),
    path('reset_pass/<active_code>', views.ResetPassword.as_view(), name='reset_password_page'),
    path('logout/', views.logoutView.as_view(), name='logout_page'),
    path('activate-account/<email_active_code>', views.ActivateAccountView.as_view(), name='activate_account'),
    path('user_history', views.ActivateAccountView.as_view(), name='activate_account'),
]
