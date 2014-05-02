# Create your views here.
import sys
import re

# Import modules
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.db import IntegrityError

# Import models
from models import Project, Sample, SampleVariable, Read, ClassificationMethod, TaxaID, ReadAssignment, ProfileSummary

# Import forms
from forms import SelectProjectForm, SearchSampleVarForm, SearchSampleProfileForm, SearchbyVariableForm, SearchbyProfileAttrForm



def home(request):
	return render(request, 'MicrobiomeExplorer/home.html')



# List All Projects 
def listProject(request):
	project_list = Project.objects.all()
	params = {
		'project_list':project_list,
		}
	return render(request, 'MicrobiomeExplorer/listProject.html', params)



# List All Samples in a Project
def listSample(request):
	if request.method == "POST":
		form = SelectProjectForm(request.POST)
		if form.is_valid():
			project_pk = request.POST['project']
			project = Project.objects.get(pk=project_pk)
			sample_list = Sample.objects.filter(project__name = project.name)
			params = {
				'form':form,
				'sample_list':sample_list,
				}
			return render(request, 'MicrobiomeExplorer/listSample.html', params)
		else:
			message = "Please select a Project."
			params = {
				'form':form,
				'message':message,
				}	
			return render(request, 'MicrobiomeExplorer/listSample.html', params)
	else:
		form = SelectProjectForm()
		params = {
			'form':form,
			}
		return render(request, 'MicrobiomeExplorer/listSample.html', params)



# View Sample Variable Information
def SampleInfo(request, samplename):
	SV_list = SampleVariable.objects.filter(sample__name = samplename)
	params = {
		'samplename' : samplename,
		'SV_list' : SV_list,
		}
	return render(request, 'MicrobiomeExplorer/SampleInfo.html', params)



# View Entire Sample Profile
def SampleProfile(request, samplename):
	PS_list = ProfileSummary.objects.filter(sample__name = samplename)
	params = {
		'samplename' : samplename,
		'PS_list' : PS_list,
		}
	return render(request, 'MicrobiomeExplorer/SampleProfile.html', params)



def SearchPage(request):
	return render(request, 'MicrobiomeExplorer/SearchPage.html')



# Search for Sample Information
def SearchSampleVar(request):
	if request.method == "POST":
		form = SearchSampleVarForm(request.POST)

		# get a list of sample objects
		sample_pk_list = request.POST.getlist('sample')
		sample_list = Sample.objects.filter(pk__in=sample_pk_list)

		# get a list of sample variable objects and save in dictionary
		sv_instance_list = request.POST.getlist('samplevariable')
		if not sv_instance_list:
			sv_instance_list = SampleVariable.objects.values_list('variable', flat=True).distinct()	
		OutputDict = {}
		for each_sample in sample_list:
			OutputDict.setdefault(each_sample, [])
			for each_sv in sv_instance_list:
				sv = SampleVariable.objects.get(sample=each_sample, variable=each_sv)
				OutputDict[each_sample].append(sv.value)

		# parameters to be rendered in the template
		params = {
			'OutputDict':OutputDict.items(),
			'sv_instance_list':sv_instance_list,
			}
		return render(request, 'MicrobiomeExplorer/SearchSampleVar.html', params)
	
	else:
		form = SearchSampleVarForm()
		params = {
			'form':form,
			}
		return render(request, 'MicrobiomeExplorer/SearchSampleVar.html', params)



# Search for Sample Profile
def SearchSampleProfile(request):
	if request.method == "POST":
		form = SearchSampleProfileForm(request.POST)

		# get a list of Sample objects
		sample_pk_list = request.POST.getlist('sample')
		sample_list = Sample.objects.filter(pk__in=sample_pk_list)
		
		# get a list of Classification Methods
		cm_pk_list = request.POST.getlist('classificationmethod')
		if not cm_pk_list:
			cm_list = ClassificationMethod.objects.all()
		else:
			cm_list = ClassificationMethod.objects.filter(pk__in=cm_pk_list)
		
		# get a list of Taxa Levels
		tl_instance_list = request.POST.getlist('taxalevel')
		if not tl_instance_list:
			tl_instance_list = TaxaID.objects.values_list('level', flat=True).distinct()

		# get a list of Attributes
		attr_instance_list = request.POST.getlist('attribute')
		if not attr_instance_list:
			attr_instance_list = ['numreads', 'perctotal', 'avgscore']


		# get a list of sample profile objects
		ps_list = []
		for each_sample in sample_list:
			for each_cm in cm_list:
				for each_tl in tl_instance_list:
					ps = ProfileSummary.objects.filter(sample=each_sample, classificationmethod=each_cm, taxaID__level=each_tl)
					ps_list.extend(ps)

		# parameters to be rendered in the template
		params = {
			'attr_instance_list':attr_instance_list,
			'ps_list':ps_list,
			}
		return render(request, 'MicrobiomeExplorer/SearchSampleProfile.html', params)
	
	else:
		form = SearchSampleProfileForm()
		params = {
			'form':form,
			}
		return render(request, 'MicrobiomeExplorer/SearchSampleProfile.html', params)




# Search Samples by Variable Values
def SearchbyVariable(request):
	if request.method == "POST":
		form = SearchbyVariableForm(request.POST)
		
		# get data from the form
		variable_instance = request.POST['samplevariable']
		comparison = request.POST['comparison']
		value = request.POST['value']

		# get a list of sample variable objects
		if comparison == "Equal To":
			sv = SampleVariable.objects.filter(variable=variable_instance, value__iexact=value)
		else:
			sv = SampleVariable.objects.filter(variable=variable_instance).exclude(value__iexact=value)
		
		# get a list of samples that satisfy the search criteria
		sample_list = []
		for each_sv in sv:
			if each_sv.sample not in sample_list:
				sample_list.append(each_sv.sample)	
		if not sample_list:
			message = "No match found! Please enter an appropriate value for the selected sample variable. "	
		else:
			message = "Here is the list of all Samples satisfying the search criteria - "	
			
		params = {
			'form':form,
			'message':message,
			'sample_list':sample_list,
			}
		return render(request, 'MicrobiomeExplorer/SearchbyVariable.html', params)
		
	else:
		form = SearchbyVariableForm()
		params = {
			'form':form,
			}
		return render(request, 'MicrobiomeExplorer/SearchbyVariable.html', params)



# Search Samples by Profile Attributes
def SearchbyProfileAttr(request):
	if request.method == "POST":
		form = SearchbyProfileAttrForm(request.POST)
		if form.is_valid():
			# get data from form
			taxaID_pk = request.POST['taxalevel']
			cm_pk = request.POST['classificationmethod']
			attr = request.POST['attribute']
			comparison = request.POST['comparison']
			value = request.POST['value']

			# get objects
			taxaID = TaxaID.objects.get(pk=taxaID_pk)
			cm = ClassificationMethod.objects.get(pk=cm_pk)
			ps_list = ProfileSummary.objects.filter(taxaID=taxaID, classificationmethod=cm)
		
			# list of samples satisfying the search criteria
			sample_list = []
			for each_ps in ps_list:
				if attr == "numreads":
					if comparison == ">":
						if float(each_ps.numreads) > float(value):
							sample_list.append(each_ps.sample)					
					elif comparison == "=":
						if float(each_ps.numreads) == float(value):
							sample_list.append(each_ps.sample)					
					elif comparison == "<":
						if float(each_ps.numreads) < float(value):
							sample_list.append(each_ps.sample)					
				elif attr == "perctotal":
					if comparison == ">":
						if float(each_ps.perctotal) > float(value):
							sample_list.append(each_ps.sample)					
					elif comparison == "=":
						if float(each_ps.perctotal) == float(value):
							sample_list.append(each_ps.sample)					
					elif comparison == "<":
						if float(each_ps.perctotal) < float(value):
							sample_list.append(each_ps.sample)					
				elif attr == "avgscore":
					if comparison == ">":
						if float(each_ps.avgscore) > float(value):
							sample_list.append(each_ps.sample)					
					elif comparison == "=":
						if float(each_ps.avgscore) == float(value):
							sample_list.append(each_ps.sample)					
					elif comparison == "<":
						if float(each_ps.avgscore) < float(value):
							sample_list.append(each_ps.sample)					
		
			if not sample_list:
				message = "No match found! Please enter an appropriate value for the selected profile attribute. "	
			else:
				message = "Here is the list of all Samples satisfying the search criteria - "	
	
			params = {
				'form':form,
				'message':message,
				'sample_list':sample_list,
				}
			return render(request, 'MicrobiomeExplorer/SearchbyProfileAttr.html', params)
		else:
			message = "Invalid form! Please make appropriate choices."	
			params = {
				'form':form,
				'message':message,
				}
			return render(request, 'MicrobiomeExplorer/SearchbyProfileAttr.html', params)
	else:
		form = SearchbyProfileAttrForm()
		params = {
			'form':form,
			}
		return render(request, 'MicrobiomeExplorer/SearchbyProfileAttr.html', params)




