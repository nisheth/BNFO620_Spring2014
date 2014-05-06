__author__ = 'BUNTY'
from django import forms
from models import Sample
from models import SampleVariable
from models import ClassificationMethod
from models import TaxaTable


class InformationSearch(forms.Form):
    sample = forms.ModelMultipleChoiceField(queryset=Sample.objects.all(), required=True)
    samplevariable = forms.ModelMultipleChoiceField(queryset=SampleVariable.objects.values('attribute').distinct().values_list('attribute', flat=True), required=True)

class ProfileSearch(forms.Form):
    
      sample = forms.ModelMultipleChoiceField(queryset=Sample.objects.all(), required= True)
      method = forms.ModelMultipleChoiceField(queryset = ClassificationMethod.objects.all(), required=True)
      taxa = forms.ModelMultipleChoiceField(queryset = TaxaTable.objects.values_list('level', flat=True).distinct(), required=False)
      profilevariable = forms.MultipleChoiceField(choices=[('numreads', 'Read Count'),
                                                         ('perctotal', 'Percent of Reads'),
                                                         ('avgscore','Average Read Score')]
                                                        , required=True)

class SearchVariable(forms.Form):
    samplevariable = forms.ModelChoiceField(queryset=SampleVariable.objects.values('attribute').distinct().values_list('attribute', flat=True), required=True)
    comparator = forms.ChoiceField(choices = [('==', '=='),
        ('!=', "!=")], required= True
    )
    searchfield = forms.CharField(required= True)

class SearchProfile (forms.Form): 
    profilevariable = forms.ChoiceField(choices=[('numreads', 'Read Count'),
                                                         ('perctotal', 'Percent of Reads'),
                                                         ('avgscore','Average Read Score')]
                                                        , required=True)
    taxalevel = forms.ModelChoiceField(queryset=TaxaTable.objects.all())
    method = forms.ModelChoiceField(queryset=ClassificationMethod.objects.all())
    comparator = forms.ChoiceField(choices = [('=','='),('>','>'),('<','<')], required = True)
    search_value = forms.FloatField(required=True)
