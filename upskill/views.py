from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from .models import Subject

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

    def get_queryset(self):
        queryset = super().get_queryset()
        subject_slug = self.kwargs.get('subject_slug')

        if subject_slug:
            queryset = queryset.filter(slug=subject_slug)

        return queryset




