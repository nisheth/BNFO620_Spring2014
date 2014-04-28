# Create your views here.
import sys
import re

# Import modules
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
#from django.contrib.auth import authenticate
#from django.contrib.auth import login as login_user
#from django.contrib.auth import logout as logout_user
#from django.contrib.auth.decorators import login_required
#from django.contrib.auth.models import User,Group,Permission
from django.db import IntegrityError

# Import models
from models import Project, Sample, SampleVariable, Read, ClassificationMethod, TaxaID, ReadAssignment, ProfileSummary

# Import forms
from forms import SearchForm


def home(request):
	return render(request, 'MicrobiomeExplorer/home.html')


def listProject(request):
	project_list = Project.objects.all()
	params = {
		'project_list':project_list,
		}
	return render(request, 'MicrobiomeExplorer/listProject.html', params)


def listSample(request):
	sample_list = Sample.objects.all()
	params = {
		'sample_list':sample_list,
		}
	return render(request, 'MicrobiomeExplorer/listSample.html', params)


def SampleInfo(request, samplename):
	SV_list = SampleVariable.objects.filter(sample__name = samplename)
	params = {
		'samplename' : samplename,
		'SV_list' : SV_list,
		}
	return render(request, 'MicrobiomeExplorer/SampleInfo.html', params)


def SampleProfile(request, samplename):
	PS_list = ProfileSummary.objects.filter(sample__name = samplename)
	params = {
		'samplename' : samplename,
		'PS_list' : PS_list,
		}
	return render(request, 'MicrobiomeExplorer/SampleProfile.html', params)


def SearchPage(request):
	if request.method == "POST":
		form = SearchForm(request.POST)
		sample_pk = request.POST['sample']
		sample = Sample.objects.get(pk=sample_pk)
		print >> sys.stderr, sample
		if form.is_valid():
			sample_list = request.POST['sample']
			print >> sys.stderr, sample_list
			params = {
				'message' : message
				}
			return render(request, 'MicrobiomeExplorer/SearchPage.html', params)
		else:
			message = "The form is invalid"
			params = {
				'message' : message
				}
			return render(request, 'MicrobiomeExplorer/SearchPage.html', params)
	else:
		form = SearchForm()
		params = {
			'form' : form
			}	
		return render(request, 'MicrobiomeExplorer/SearchPage.html', params)
























