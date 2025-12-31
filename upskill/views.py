from django.views import View
from django.views.generic import ListView, TemplateView, DetailView

from .forms import ContactForm
from .models import Subject, Course, Module, Content

import os
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from .models import File, Content
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .forms import ContactForm


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        return context

class CourseDetail(DetailView):
    template_name = 'upskill/detail.html'
    queryset = Course.objects.all()
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        course = self.get_object()
        context = super().get_context_data(**kwargs)
        context['modules'] = enumerate(course.modules.all(), start=1)
        return context

class ContentDetailView(DetailView):
    template_name = 'upskill/content_detail.html'
    context_object_name = 'content'
    model = Content



def download_file(request, content_id):
    content = get_object_or_404(Content, id=content_id)


    if content.content_type.model != 'file':
        raise Http404("Not a file content")

    file_item = content.item  # bu File model

    file_path = file_item.file.path
    file_name = os.path.basename(file_path)

    response = FileResponse(
        open(file_path, 'rb'),
        as_attachment=True,
        filename=file_name
    )

    return response



def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            full_message = f"Message from {name} ({email}):\n\n{message}"

            send_mail(
                subject,
                full_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            messages.success(request, "Your message has been sent successfully!")
            return redirect('upskill/contact')
    else:
        form = ContactForm()
    return render(request, 'upskill/contact.html', {'form': form})
