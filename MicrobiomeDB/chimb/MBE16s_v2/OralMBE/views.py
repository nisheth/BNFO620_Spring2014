from django.shortcuts import render
import codecs
import sys
import collections
from django import forms
from forms import sampleInfoForm
from forms import profileInfoForm
from forms import searchbyAttribute
from forms import searchbyTaxa
from django.db.models import Q
from models import Project
from models import Sample
from models import SampleAttribute
from models import ClassificationMethod
from models import Taxa
from models import ProfileSummary
# Create your views here.



#######################################################################
def home(request):
    return render(request, 'base.html')




#######################################################################
def sampleInfo(request):

    if request.method == 'POST':
        form = sampleInfoForm(request.POST)

        if request.POST.getlist('sampleChoice') and request.POST.getlist('attributeChoice'):
            sample_pk_List = request.POST.getlist('sampleChoice')
            sampleList = Sample.objects.filter(pk__in=sample_pk_List)
            attributeList = request.POST.getlist('attributeChoice')



            sampleAttributeDict = {}
            for sample in sampleList:

                for attribute in attributeList:


                   # print attribute, type(attribute)
                    attributeObj = SampleAttribute.objects.get(sample=sample, attribute=attribute)
                    attributeValue = attributeObj.value
                    samplename = sample.name
                    samplename = samplename.encode('ascii', 'ignore')
                    if samplename not in sampleAttributeDict:
                        sampleAttributeDict[samplename] = []
                    sampleAttributeDict[samplename].append(attributeValue)

            #print sampleAttributeDict
            sortedSAD = collections.OrderedDict(sorted(sampleAttributeDict.items()))

            message = 'Here are your samples and their attributes that you\'ve selected'
            params = {
                'form': form,
                'message': message,
				'sampleAttributeDict': sortedSAD,
				'attributeList': attributeList
            }

            return render(request,'sampleInfo.html',params)


        else:
            message = 'Form is not valid. Please choose one or more samples and variables to view.'
            form = sampleInfoForm()
            params = {
                'message': message,
                'form': form
            }
            return render (request,'sampleInfo.html',params)

    else:
        form = sampleInfoForm()
        params = {
            'form' : form
        }
        return render (request,'sampleInfo.html',params)


#######################################################################
def profileInfo(request):

    if request.method == 'POST':
        form = profileInfoForm(request.POST)

        if request.POST.getlist('sampleChoice') and request.POST['taxalevelChoice'] and request.POST['methodChoice'] and request.POST['profileVariable']:
            sample_pk_List = request.POST.getlist('sampleChoice')
            sampleList = Sample.objects.filter(pk__in=sample_pk_List)
            taxalevel = request.POST['taxalevelChoice']
            methodpk = request.POST['methodChoice']
            method = ClassificationMethod.objects.get(key=methodpk)
            variable = request.POST['profileVariable']


            #print sampleList
            #print taxalevel
            #print method.key
            #print variable

            taxalist = Taxa.objects.filter(level=taxalevel)
            profileList = []
            for sample in sampleList:
                for taxa in taxalist:
                    if ProfileSummary.objects.filter(sample=sample,
                                                classificationmethod=method,
                                                taxa=taxa).exists():
                        profileList.append(ProfileSummary.objects.get(sample=sample,
                                                classificationmethod=method,
                                                taxa=taxa))
            #print profileList


            message = 'Here is the profile data for samples and taxonomy level that you have chosen:'
            params = {
                'form': form,
                'message': message,
                'profileList': profileList,
                'variable': variable,
                'taxalevel': taxalevel
				#'sampleAttributeDict': sortedSAD,
				#'attributeList': attributeList
            }

            return render(request,'profileInfo.html',params)


        else:
            message = 'Form is not valid. Please make or enter a choice in each field below.'
            form = profileInfoForm()
            params = {
                'message': message,
                'form': form
            }
            return render (request,'profileInfo.html',params)

    else:
        form = profileInfoForm()
        params = {
            'form' : form
        }
        return render (request,'profileInfo.html',params)


#######################################################################
def compareAttribute(request):

    if request.method == 'POST':
        form = searchbyAttribute(request.POST)

        if request.POST['attributeChoice'] and request.POST['comparisonType'] and request.POST['valueChoice']:

            attribute = request.POST['attributeChoice']
            comparator = request.POST['comparisonType']
            value = request.POST['valueChoice']

            if comparator == 'Equal To':
                sampleAttributeList = SampleAttribute.objects.filter(attribute=attribute, value__iexact=value)

            if comparator == 'Not Equal To':
                sampleAttributeList = SampleAttribute.objects.filter(attribute=attribute).exclude(value__iexact=value)

            sampleList = []

            for sampleAttribute in sampleAttributeList:
                if sampleAttribute.sample not in sampleList:
                    sampleList.append(sampleAttribute.sample)


            message = 'Here are the samples that satisfy your condition:'
            condition = str(attribute) + " | " + str(comparator) + " | " + str(value)

            params = {
                'form': form,
                'condition': condition,
                'message': message,
				'sampleList': sampleList

            }

            return render(request,'searchbyAttribute.html',params)


        else:
            message = 'Form is not valid. Please select a value for all fields.'
            form = searchbyAttribute()
            params = {
                'message': message,
                'form': form
            }
            return render (request,'searchbyAttribute.html',params)

    else:
        form = searchbyAttribute()
        params = {
            'form' : form
        }
        return render (request,'searchbyAttribute.html',params)

#######################################################################
def compareTaxa(request):

    if request.method == 'POST':
        form = searchbyTaxa(request.POST)

        if form.is_valid():
            taxapk = request.POST['taxaChoice']
            taxa = Taxa.objects.get(pk=taxapk)
            methodpk = request.POST['methodChoice']
            method = ClassificationMethod.objects.get(key=methodpk)
            variable = request.POST['profileVariable']
            threshold = request.POST['threshold']

            #print taxa
            #print method.key
            #print variable
            #print threshold

            sampleList = []

            profileList = ProfileSummary.objects.filter(taxa=taxa, classificationmethod=method)

            for profile in profileList:
                if variable=='Read Count':
                    if float(profile.numreads) > float(threshold):
                        sampleList.append(profile.sample)

                if variable=='Percent of Reads':
                    if float(profile.perctotal) > float(threshold):
                        sampleList.append(profile.sample)

                if variable=='Average Read Score':
                    if float(profile.avgscore) > float(threshold):
                        sampleList.append(profile.sample)

            #print profileList
            #print sampleList

            message = 'Here are the samples that satisfy your condition:'
            condition = str(variable) + " > " + str(threshold) + " for the " + str(taxa.level) + " " + str(taxa.name) + " using Classification Method " + str(method.key)
            params = {
                'form': form,
                'condition': condition,
                'message': message,
				'sampleList': sampleList

            }

            return render(request,'searchbyTaxa.html',params)


        else:
            message = 'Form is not valid. Please enter or select a value for all fields.'
            form = searchbyTaxa()
            params = {
                'message': message,
                'form': form
            }
            return render (request,'searchbyTaxa.html',params)

    else:
        form = searchbyTaxa()
        params = {
            'form' : form
        }
        return render (request,'searchbyTaxa.html',params)
