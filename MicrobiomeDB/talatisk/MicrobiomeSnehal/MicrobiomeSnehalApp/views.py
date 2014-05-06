from django.shortcuts import render
from MicrobiomeSnehalApp.models import Project, Sample, SampleVariable, ProfileSummary, ClassificationMethod, TaxaTable
from forms import InformationSearch, ProfileSearch, SearchVariable, SearchProfile
from django.shortcuts import redirect
from django.http import HttpResponse

import sys


def home(request):
    return render(request, 'home.html')

def projects(request):
    projectList = Project.objects.all()
    params = {
        'projectList':projectList,
        }
    return render(request, 'projects.html', params)
        
def samples(request):
    sampleList = Sample.objects.all()
    params = {
        'sampleList': sampleList,
    }
    return render(request, "samples.html", params)       

def showInfo(request):
    if request.method == 'POST':
        form = InformationSearch(request.POST)
        samplepk_list = request.POST.getlist('sample')
        sample_list = Sample.objects.filter(pk__in=samplepk_list)
        svlist = request.POST.getlist('samplevariable')
        sampleVariable = {}
        for sample in sample_list:
            for attribute in svlist:
                obj_attribute = SampleVariable.objects.get(sample=sample, attribute=attribute)
                att_value = obj_attribute.value
                if sample not in sampleVariable:
                    sampleVariable[sample] = []
                sampleVariable[sample].append(att_value)

        message = "Thank you for your submission but make sure *fields are selected if not table is returned"
        params = {
            'form': form,
            'message': message,
            'sampleVariable': sampleVariable,
            'svlist': svlist
        }
        return render(request, 'showInfo.html', params)


    else:
        form = InformationSearch()
        params = {
            'form': form
        }
        return render(request, 'showInfo.html', params)


##____________________________________________________________________________________________________________________##

def showProfile(request):
    if request.method == "POST":
		form = ProfileSearch(request.POST)
		sample_pk_list = request.POST.getlist('sample')
		sample_list = Sample.objects.filter(pk__in=sample_pk_list)
		class_list = request.POST.getlist('classificationmethod')
		if not class_list:
			methodList = ClassificationMethod.objects.all()
		else:
			methodList = ClassificationMethod.objects.filter(pk__in=class_list)
		taxaList = request.POST.getlist('taxa')
		if not taxaList:
			taxaList = TaxaTable.objects.values_list('level', flat=True).distinct()
		variableList = request.POST.getlist('profilevariable')
		if not variableList:
			variableList = ['numreads', 'perctotal', 'avgscore']
		profile_summary = []
		for sample in sample_list:
			for method in methodList:
				for taxa in taxaList:
					profilesummary = ProfileSummary.objects.filter(sample=sample, classificationmethod=method, taxaID__level=taxa)
					profile_summary.extend(profilesummary)
                
		params = {
			'variableList':variableList,
			'profile_summary':profile_summary,
			}
		return render(request, 'showProfile.html', params)

    else:
		form = ProfileSearch()
		params = {
			'form':form,
			}
		return render(request, 'showProfile.html', params)

##______________________________________________________________________________________________________________________##
                
def variablesearch(request):
    if request.method == "POST":
        form = SearchVariable(request.POST)
        variable = request.POST['samplevariable']
        comparator = request.POST['comparator']
        value = request.POST['searchfield']

        if comparator == "==":
            samplelist = SampleVariable.objects.filter(attribute=variable, value__iexact=value)

        elif comparator == '!=':
            samplelist = SampleVariable.objects.filter(attribute=variable).exclude(value__iexact=value)

        samlist = []

        for sample in samplelist:
            if sample.sample not in samlist:
                samlist.append(sample.sample)

        if not samplelist:
            message = "No Match Found Please Try Again"
        else:
            message = "Here are the results obtained from your query"

        params = {
             'form': form,
            'samlist': samlist,
             'message':message,
        }

        return render(request, 'searchVariable.html', params)

    else:
        form = SearchVariable()
        params = {
            'form': form,
        }
        return render(request, 'searchVariable.html', params)
                    

##____________________________________________________________________________________________________________________

def profileSearch(request):
    if request.method == "POST":
        form = SearchProfile(request.POST)
        if form.is_valid():
            profilevar = request.POST['profilevariable']
            comparator = request.POST['comparator']
            searchField = request.POST['search_value']
            taxaInfo = request.POST['taxalevel']
            methodInfo = request.POST['method']
            taxaID = TaxaTable.objects.get(pk=taxaInfo)
            class_method = ClassificationMethod.objects.get(pk=methodInfo)
            profile_sumlist = ProfileSummary.objects.filter(taxaID=taxaID, classificationmethod=class_method)

            sampleList = []
            for profilesum in profile_sumlist:
                if ((profilevar == "perctotal") & (float(profilesum.perctotal) == float(searchField)) & (comparator == "=")):
                    sampleList.append(profilesum.sample)
                elif ((profilevar == "perctotal") & (float(profilesum.perctotal) > float(searchField)) & (comparator == ">")):
                    sampleList.append(profilesum.sample)
                elif ((profilevar == "perctotal") & (float(profilesum.perctotal) < float(searchField)) & (comparator == "<")):
                    sampleList.append(profilesum.sample)
                elif ((profilevar == "avgscore") & (float(profilesum.avgscore) == float(searchField)) & (comparator == "=")):
                    sampleList.append(profilesum.sample)
                elif ((profilevar == "avgscore") & (float(profilesum.avgscore) < float(searchField)) & (comparator == "<")):
                    sampleList.append(profilesum.sample)
                elif ((profilevar == "avgscore") & (float(profilesum.perctotal) > float(searchField)) & (comparator == ">")):
                    sampleList.append(profilesum.sample)
                elif ((profilevar == "numreads") & (float(profilesum.numreads) == float(searchField)) & (comparator == "=")):
                    sampleList.append(profilesum.sample)
                elif ((profilevar == "numreads") & (float(profilesum.numreads) < float(searchField)) & (comparator == "<")):
                    sampleList.append(profilesum.sample)
                elif ((profilevar == "numreads") & (float(profilesum.numreads) > float(searchField)) & (comparator == ">")):
                    sampleList.append(profilesum.sample)


            if not sampleList:
                message = "No match was found. Please try again."
            else:
                message = "Here is the list of samples that were obtained based on your query"

            params = {
                'form':form,
                'message':message,
                'sampleList':sampleList,
                }
            return render(request, 'searchProfile.html', params)

        else:
            message = "Invalid submission please try again"
            params = {
                'form':form,
                'message':message,
                }
            return render (request, 'searchProfile.html', params)

    else:
        form = SearchProfile()
        params = {
            'form':form,
             }
        return render(request, 'searchProfile.html', params)

                
















