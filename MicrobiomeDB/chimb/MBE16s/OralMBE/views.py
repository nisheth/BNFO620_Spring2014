from django.shortcuts import render
import codecs
import sys
from OralMBE.models import Project
from OralMBE.models import Sample
# Create your views here.

def home(request):
    return render(request, 'home.html')

def profiles(request):
    projectlist = Project.objects.all()
    params = {
        'projectlist': projectlist,
        }
    return render(request, 'projects.html', params)

def samples(request):
    samplelist = Sample.objects.all()
    params = {
        'samplelist': samplelist,
        }
    return render(request, 'samples.html', params)