from django.urls import path
from .views import IndexView, AboutView, CourseView, CourseDetail
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('subject/<slug:subject_slug>', IndexView.as_view(), name='course_of_subjects'),
    path('about/', AboutView.as_view(), name='about'),
    path('courses/', CourseView.as_view(), name='courses'),
    path('course/<slug:slug>/detail/', CourseDetail.as_view(), name='detail'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)