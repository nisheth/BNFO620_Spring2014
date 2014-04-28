from django import forms
from models import Project
from models import Sample
from models import SampleAttribute
from models import ClassificationMethod
from models import Taxa
from models import ProfileSummary

class sampleInfoForm(forms.Form):
    sampleChoice = forms.ModelMultipleChoiceField(queryset=Sample.objects.all(), required=True)
    attributeChoice = forms.ModelMultipleChoiceField(queryset=SampleAttribute.objects.values_list('attribute', flat=True).distinct(), required=True)




class profileInfoForm(forms.Form):
    sampleChoice = forms.ModelMultipleChoiceField(queryset=Sample.objects.all(), required=True)
    taxalevelChoice = forms.ModelMultipleChoiceField(queryset=Taxa.objects.values_list('level', flat=True).distinct(), required=True)


    methodChoice = forms.ModelChoiceField(queryset=ClassificationMethod.objects.all(), required=True)
    profileVariable = forms.ChoiceField(choices=[('Read Count', 'Read Count'),
                                                         ('Percent of Reads', 'Percent of Reads'),
                                                         ('Average Read Score','Average Read Score')]
                                                , required=True)



class searchbyAttribute (forms.Form):
    attributeChoice = forms.ModelChoiceField(queryset=SampleAttribute.objects.values_list('attribute', flat=True).distinct(), required=True)
    comparisonType = forms.ChoiceField(choices=[('Equal To', 'Equal To'),
                                                ('Not Equal To', 'Not Equal To')],
                                                required=True)
    valueChoice = forms.CharField(required=True)

class searchbyTaxa (forms.Form):
    taxaChoice = forms.ModelChoiceField(queryset=Taxa.objects.all(), required=True)
    methodChoice = forms.ModelChoiceField(queryset=ClassificationMethod.objects.all(), required=True)
    profileVariable = forms.ChoiceField(choices=[('Read Count', 'Read Count'),
                                                         ('Percent of Reads', 'Percent of Reads'),
                                                         ('Average Read Score','Average Read Score')]
                                                , required=True)
    threshold = forms.FloatField(required=True)



