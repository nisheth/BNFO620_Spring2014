from django import forms
from models import Sample, SampleVariable, ClassificationMethod, TaxaID


class SearchForm(forms.Form):

	sample = forms.ModelMultipleChoiceField(queryset=Sample.objects.all())
	samplevariable = forms.ModelMultipleChoiceField(queryset=SampleVariable.objects.values('variable').distinct())
	classificationmethod = forms.ModelMultipleChoiceField(queryset=ClassificationMethod.objects.all())
	taxalevel = forms.ModelMultipleChoiceField(queryset=TaxaID.objects.values('level').distinct())


