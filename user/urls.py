from django.urls import path
from .views import home_view, user_login, user_logout, register, activate

urlpatterns = [
    path('register/', register, name='register'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('', home_view, name='home'),

]
