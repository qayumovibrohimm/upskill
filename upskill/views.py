from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, TemplateView, DetailView

from .models import Subject, Course

# Create your views here.


# def index(request):
#     return render(request, 'upskill/index.html')

# class IndexView(View):
#
#     def get(self, request, subject_slug = None):
#
#         if subject_slug is None:
#             subjects = Subject.objects.all()
#
#         context = {
#             'subjects':subjects
#         }
#         return render(request,'upskill/index.html')


class IndexView(ListView):
    model = Subject
    template_name = 'upskill/index.html'
    context_object_name = 'subjects'
    ordering = ['id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        subject_slug = self.kwargs.get('subject_slug')

        courses = Course.objects.all()

        if subject_slug:
            courses = courses.filter(subject__slug = subject_slug)

        context['courses'] = courses

        return context


    def get_queryset(self):
        queryset = super().get_queryset()
        subject_slug = self.kwargs.get('subject_slug')

        if subject_slug:
            queryset = queryset.filter(slug=subject_slug)

        return queryset


class AboutView(TemplateView):
    template_name = 'upskill/about.html'



class CourseView(TemplateView):
    template_name = 'upskill/course.html'


class CourseDetailsView(DetailView):
    model = Course
    template_name = 'upskill/detail.html'
    context_object_name = 'course'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_courses'] = Course.objects.exclude(pk=self.object.pk).order_by('-created_at')[:5]
        context['related_courses'] = Course.objects.filter(subject=self.object.subject).exclude(pk=self.object.pk)[:5]
        context['categories'] = Subject.objects.all()
        return context