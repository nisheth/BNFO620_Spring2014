from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login 
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,Group,Permission
from django.db import IntegrityError

from models import Project
from models import Sample
from models import SampleVariable
from models import Method
from models import ProfileSummary
from models import Taxonomy

import sys
import re

def Sample_list(request):
    sample_list = Sample.objects.all()
    params = {
        'sample_list' : sample_list,
        }
    return render(request, 'Sample.html', params)

def Project_list(request):
    project_list = Project.objects.all()
    params = {
        'project_list' : project_list,
        }
    return render(request, 'Project.html', params)

def Home(request):
    return render(request,'home.html')
