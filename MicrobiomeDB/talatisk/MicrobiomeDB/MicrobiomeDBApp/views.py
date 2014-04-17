from django.shortcuts import render
from MicrobiomeDBApp.models import Project, Sample
import sys

def home(request):
    return render(request, 'home.html')

def projects(request):
        project = Project.objects.all()
        params = {
        'project': project,
         }
        return render(request, "projects.html", params)

def samples(request):
        sample = Sample.objects.all()
        params = {
        'sample': sample,
         }
        return render(request, "samples.html", params)