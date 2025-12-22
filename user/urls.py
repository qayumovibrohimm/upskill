from django.urls import path
from .views import register_page, verify_email_code
from django.conf import settings
from django.conf.urls.static import static

app_name = 'user'

urlpatterns = [
    path('register/', register_page, name='register_page'),
    path('email-confirm/<uidb64>/<token>/', verify_email_code, name='verify-email-confirm'),
    path('verify-code/', verify_email_code, name='verify-code'),

]