import sys
import re
import collections
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

from forms import attr_select_form
from forms import profile_select_form
from forms import attr_search_form
from forms import prof_search_form


########## Method to display all the samples ##########
def Sample_list(request):
    sample_list = Sample.objects.all()
    params = {
        'sample_list' : sample_list,
        }
    return render(request, 'Sample.html', params)


########## Method to display all the projects ##########
def Project_list(request):
    project_list = Project.objects.all()
    params = {
        'project_list' : project_list,
        }
    return render(request, 'Project.html', params)


########## Method to display all the variables and their values ##########
def Variables(request):
    var_list = SampleVariable.objects.all()
    params = {
        'var_list' : var_list,
        }
    return render(request, 'Variables.html', params)


########## Method to display all the variables and their values based on users request ##########
def AttributeInfo(request):
    if request.method == 'POST':
        form = attr_select_form(request.POST)  

        # Obtaining the user inputs
        samples = request.POST.getlist('samples')
        #print >>sys.stderr, samples
        variable_list = request.POST.getlist('variables')
        #print >>sys.stderr, variable_list

        # Creating another list with only those samples from the sample model which have the same primary key as requested by the user.
        sample_list = Sample.objects.filter(pk__in = samples)
        #print >>sys.stderr, sample_list

        # Creating an empty dictionary to store all the required data.
        sampleVariableDict = {}

        # Iterating through the sample and variable list
        for sample in sample_list:
            for variable in variable_list:
                # Obtaining the specific objects based on user input
                variable_object = SampleVariable.objects.get(sample = sample, variable = variable)
                # Obtaining the values of those filtered objects
                variable_value = variable_object.value
                # Obtaining the name of those samples
                sample_name = sample.name
                # Checking for the presence of those sample in the dictionary 
                if sample_name not in sampleVariableDict:
                    # If the sample is not present, adding them into the dictionary as new keys.
                    sampleVariableDict[sample_name] = []

                # Appending the value of each variable requested     
                sampleVariableDict[sample_name].append(variable_value)

        #print sampleVariableDict

        # Message for telling the user what the results contain.
        if not sampleVariableDict:
            message = "No results found!"
        else:    
            message = "The values for the respective samples and variables selected by you are:"

        # Parameters to be used in the html file
        params = {
                'form': form,
                'message': message,
		'sampleVariableDict': sampleVariableDict,
		'variable_list': variable_list,
                }
        # Rendering the request to the respective html template.
        return render(request,'AttributeInfo.html',params)

    # If request method is not post, do this!
    else:
        form = attr_select_form()
        params = {
            'form' : form,
        }
        return render (request,'AttributeInfo.html',params)
    
        
########## Method to display profile information based on the users request ##########
def ProfileInfo(request):
    if request.method == 'POST':
        form = profile_select_form(request.POST)

        # Obtaining the user inputs
        samples = request.POST.getlist('samples')
        taxa_level = request.POST['taxa']
        #print >>sys.stderr, taxa_level
        methods = request.POST['method']
        variables = request.POST['variables']
        #print >>sys.stderr, variables

        # Creating other variables to hold certin required data
        method = Method.objects.get(id = methods)
        #print >>sys.stderr, method.id
        sample_list = Sample.objects.filter(pk__in = samples)
        #print >>sys.stderr, sample_list
        taxa_list = Taxonomy.objects.filter(level = taxa_level)

        # Creating an empty list which will hold the results for what the user requests
        profile_list = []

        # Looping through the taxa and sample lists
        for taxa in taxa_list:
            for sample in sample_list:
                # Filtering the required data
                to_check = ProfileSummary.objects.filter(sample = sample, method = method, taxa_Id = taxa)
                # Checking to see if the data exists
                if to_check.exists():
                    # Adding the data to the empty list previously created. 
                    profile_list.append(ProfileSummary.objects.get(sample = sample, method = method, taxa_Id = taxa))
                    #print profile_list

        # Message for telling the user what the results contain.
        if not profile_list:
            message = "No results found!"
        else:    
            message = "This is the profile data for the chosen attributes:"

        # Parameters to be used in the html file
        params = {
            'form': form,
            'message': message,
            'variables': variables,
            'profile_list': profile_list,
            'taxa_level': taxa_level,
            }

        # Rendering the request to the respective html template.
        return render(request,'ProfileInfo.html',params)

    # If request method is not post, do this!
    else:
        form = profile_select_form()
        params = {
            'form': form,
            }
        return render(request,'ProfileInfo.html',params)
    

########## Method to display all the filtered samples from SampleVariable model based on users request ##########
def SearchVariable(request):
    if request.method == 'POST':
        form = attr_search_form(request.POST)

        # Obtaining the user unputs
        variable = request.POST['variables']
        #print >>sys.stderr, variable
        comparison = request.POST['comparison']
        #print >>sys.stderr, comparison
        value = request.POST['values']
        #print >>sys.stderr, value

        # Creating an empty list to hold all the filtered samples
        sample_list = []

        # If comparison chosen by user is "Equal to", fill the list wih objects that have the exact values
        if comparison == 'Equal to':
            sample_list = SampleVariable.objects.filter(variable = variable, value__iexact = value)

        # Else, fill the list with value that are not the same
        if comparison == 'Not equal to':
            sample_list = SampleVariable.objects.filter(variable = variable).exclude(value__iexact = value)

        # Creating a string of what the search criteria was.
        if not value:
            condition = ""
        else:    
            condition = str(variable) + " which are " + str(comparison) + " the value of " + str(value)    

        # Message for telling the user what the results contain.
        if not sample_list:
            message = "Please select the value!"
        else:    
            message = "Here are the samples that satisfy your condition:"

        # Parameters to be used in the html file
        params = {
            'form': form,
            'condition': condition,
            'message': message,
            'sample_list': sample_list,
            }

        # Rendering the request to the respective html template.
        return render(request,'SearchVariable.html',params)

    # If request method is not post, do this!
    else:
        form = attr_search_form()
        params = {
            'form' : form,
        }
        return render (request,'SearchVariable.html',params)

    
########## Method to display all the filtered samples from ProfileSummary model based on users request ##########
def SearchProfile(request):
    if request.method == 'POST':
        form = prof_search_form(request.POST)

        # Obatining all the user inputs
        taxas = request.POST['taxa']
        method = request.POST['method']
        #print >>sys.stderr, method
        variable = request.POST['variables']
        #print >>sys.stderr, variable
        threshold = request.POST['threshold']
        #print >>sys.stderr, threshold

        # Creating a new variable to hold all the taxa objects which have the same primary key as requested by the user.
        taxa = Taxonomy.objects.get(pk = taxas)
        #print >>sys.stderr, taxa

        # Creating a list with only those objects from the profile summary model that the user has specified 
        profile_list = ProfileSummary.objects.filter(taxa_Id = taxa, method = method)

        # Creating n empty list to hold all the sampes that are filtered
        sample_list = []

        # Iterating through the profile_list
        for profile in profile_list:
            if threshold:
                # Appending to sample_list based on the variable and threshold requested
                if variable == 'Number of reads' and float(profile.num_of_reads) > float(threshold):
                    sample_list.append(profile.sample)

                if variable == 'Percentage' and float(profile.percentage) > float(threshold):
                    sample_list.append(profile.sample)

                if variable == 'Average score' and float(profile.avg_score) > float(threshold):
                    sample_list.append(profile.sample)

        #print >>sys.stderr, profile_list
        #print >>sys.stderr, sample_list

        # Creating a string of what the search criteria was.
        if not threshold:
            condition = ""
        else:    
            condition = str(variable) + " greater than " + str(threshold) + " for the " + str(taxa.level) + " of " + str(taxa.name) + " using Classification Method " + str(method)        
                
        # Message for telling the user what the results contain.
        if not sample_list:
            message = "Please enter threshold!"
        else:    
            message = 'Here are the samples that satisfy your condition:'

        # Parameters to be used in the html file
        params = {
            'form': form,
            'condition': condition,
            'message': message,
            'sample_list': sample_list,
            }

        # Rendering the request to the respective html template.
        return render(request,'SearchProfile.html',params)

    # If request method is not post, do this!
    else:
        form = prof_search_form()
        params = {
            'form' : form,
        }
        return render (request,'SearchProfile.html',params)

    
########## Method to display the home page ##########    
def Home(request):
    return render(request,'home.html')
