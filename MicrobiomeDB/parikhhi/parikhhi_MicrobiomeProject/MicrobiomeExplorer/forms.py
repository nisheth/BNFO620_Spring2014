from django import forms
from models import Project, Sample, SampleVariable, ClassificationMethod, TaxaID

class SelectProjectForm(forms.Form):
	project = forms.ModelChoiceField(queryset=Project.objects.all())


class SearchSampleVarForm(forms.Form):
	sample = forms.ModelMultipleChoiceField(queryset=Sample.objects.all())
	samplevariable = forms.ModelMultipleChoiceField(queryset=SampleVariable.objects.values_list('variable', flat=True).distinct(), required=False)


class SearchSampleProfileForm(forms.Form):
	USERTYPE_CHOICES = (
		('numreads', 'Number of Reads'),
		('perctotal', 'Percentage of Total'),
		('avgscore', 'Average Score'),
	)	

	sample = forms.ModelMultipleChoiceField(queryset=Sample.objects.all())
	classificationmethod = forms.ModelMultipleChoiceField(queryset=ClassificationMethod.objects.all(), required=False)
	taxalevel = forms.ModelMultipleChoiceField(queryset=TaxaID.objects.values_list('level', flat=True).distinct(), required=False)
	attribute = forms.MultipleChoiceField(choices=USERTYPE_CHOICES, required=False)


class SearchbyVariableForm(forms.Form):
	samplevariable = forms.ModelChoiceField(queryset=SampleVariable.objects.values_list('variable', flat=True).distinct(), required=False)	
	comparison = forms.ChoiceField([('Equal To','Equal To'),('Not Equal To', 'Not Equal To')], required=True)
	value = forms.CharField(required=True)


class SearchbyProfileAttrForm(forms.Form):
	USERTYPE_CHOICES = (
		('numreads', 'Number of Reads'),
		('perctotal', 'Percentage of Total'),
		('avgscore', 'Average Score'),
	)	

	taxalevel = forms.ModelChoiceField(queryset=TaxaID.objects.all())
	classificationmethod = forms.ModelChoiceField(queryset=ClassificationMethod.objects.all())
	attribute = forms.ChoiceField(choices=USERTYPE_CHOICES)
	comparison = forms.ChoiceField([('>','>'), ('=','='),('<','<')], required=True)
	value = forms.FloatField(required=True)
	
	


