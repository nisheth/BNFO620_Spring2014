import sys
from django import forms
from django.forms.fields import ChoiceField
from django.forms.fields import MultipleChoiceField
from django.forms.widgets import RadioSelect
from django.forms.widgets import CheckboxSelectMultiple
from django.forms.extras.widgets import SelectDateWidget
from models import SampleVariable
from models import ProfileSummary
from models import Sample
from models import Taxonomy
from models import Method

num_of_reads = "Number of reads"
percentage = "Percentage"
avg_score = "Average score"
VARIABLE_CHOICES = (
    (num_of_reads, "Number of reads"),
    (percentage, "Percentage"),
    (avg_score, "Average score"),
    )


method_1 = "1"
method_2 = "2"
METHOD_CHOICES = (
    (method_1, "1"),
    (method_2, "2"),
    )


equal = "Equal to"
not_equal = "Not equal to"
SEARCH_CHOICES = (
    (equal, "Equal to"),
    (not_equal, "Not equal to"),
    )

##sampleVariableList = []
##all_ = SampleVariable.objects.all()
##for sample in all_:
##    choice = (sample.variable,sample.variable)
##    sampleVariableList.append(choice)
##
##final = sampleVariableList[0:37]    
##print >> sys.stderr, final
##
##class attr_select_form(forms.Form):
##    #attributes = forms.MultipleChoiceField (required = False, widget = CheckboxSelectMultiple(), choices = CHECKBOX_CHOICES)
##    def __init__(self, sample, variable, *args, **kwargs):
##        super(attr_select_form, self).__init__(*args, **kwargs)
##        self.fields['Variables'] = forms.MultipleChoiceField(widget = CheckboxSelectMultiple(), choices=[(o.variable, str(o)) for o in SampleVariable.objects.filter(id__in = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37])])
##        self.fields['Samples'] = forms.MultipleChoiceField(required = True, widget = CheckboxSelectMultiple(), choices=[(o.sample, str(o)) for o in SampleVariable.objects.filter(variable = variable)])
##
##class prof_select_form(forms.Form):
##    def __init__(self, sample, method, taxa_Id, *args, **kwargs):
##        super(attr_select_form, self).__init__(*args, **kwargs) 
##        self.fields['Samples'] = forms.MultipleChoiceField(required = True, widget = CheckboxSelectMultiple(), choices=[(o.sample, str(o)) for o in ProfileSummary.objects.filter(sample = sample)])
##        self.fields['Method'] = forms.MultipleChoiceField(widget = CheckboxSelectMultiple(), choices=[(o.method, str(o)) for o in ProfileSummary.objects.filter(method = method)])
##        self.fields['Taxa_ID'] = forms.MultipleChoiceField(widget = CheckboxSelectMultiple(), choices=[(o.taxa_Id, str(o)) for o in ProfileSummary.objects.filter(taxa_Id = taxa_Id)])
##        self.fields['Variables'] = forms.MultipleChoiceField(widget = CheckboxSelectMultiple(), choices = CHECKBOX_CHOICES)

class attr_select_form(forms.Form):
    samples = forms.ModelMultipleChoiceField(queryset = Sample.objects.all(), required = True)
    variables = forms.ModelMultipleChoiceField(queryset = SampleVariable.objects.values('variable').distinct().values_list('variable', flat = True), required = True)

class profile_select_form(forms.Form):
    samples = forms.ModelMultipleChoiceField(queryset = Sample.objects.all(), required = True)
    method = forms.ModelChoiceField(queryset = Method.objects.all(), required = True)
    taxa = forms.ModelMultipleChoiceField(queryset = Taxonomy.objects.values('level').distinct().values_list('level', flat = True), required = True)
    variables = forms.MultipleChoiceField(choices = VARIABLE_CHOICES, required = True)

class attr_search_form(forms.Form):
    variables = forms.ModelMultipleChoiceField(queryset = SampleVariable.objects.values('variable').distinct().values_list('variable', flat = True))
    comparison = forms.MultipleChoiceField(choices = SEARCH_CHOICES)
    values = forms.CharField(required = True)

class prof_search_form(forms.Form):
    taxa = forms.ModelMultipleChoiceField(queryset = Taxonomy.objects.all(), required=True)
    method = forms.ModelChoiceField(queryset = Method.objects.all(), required = True)
    variables = forms.MultipleChoiceField(choices = VARIABLE_CHOICES, required = True)
    threshold = forms.FloatField(required=True)    
