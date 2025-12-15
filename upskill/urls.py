from django.urls import path

from .views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    # path('subject/<slug:subject_slug>', IndexView.as_view(), name='courses_of_subject')

]