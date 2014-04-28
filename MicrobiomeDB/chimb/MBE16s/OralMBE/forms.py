from django import forms
from models import Project
from models import Sample
from models import SampleAttribute
from models import ClassificationMethod
from models import Taxa
from models import ProfileSummary

class sampleInfoForm(forms.Form):
    sampleChoice = forms.ModelMultipleChoiceField(queryset=Sample.objects.all(), required=True)
    attributeChoice = forms.MultipleChoiceField(choices=[                                                    ('site', 'site'),
                                                         ('run_date', 'run_date'),
                                                         ('patientID', 'patientID'),
                                                         ('depth', 'depth'),
                                                         ('barcode', 'barcode'),
                                                         ('Tooth-S', 'Tooth-S'),
                                                         ('Tooth-D', 'Tooth-D'),
                                                         ('Surf-S', 'Surf-S'),
                                                         ('Surf-D', 'Surf-D'),
                                                         ('Smoke/Pk Yrs', 'Smoke/Pk Yrs'),
                                                         ('Race', 'Race'),
                                                         ('Periodontol Dz DX', 'Periodontol Dz DX'),
                                                         ('PI-S', 'PI-S'),
                                                         ('PI-D', 'PI-D'),
                                                         ('PD-S', 'PD-S'),
                                                         ('PD-D', 'PD-D'),
                                                         ('Mobility-S', 'Mobility-S'),
                                                         ('Mobility-D', 'Mobility-D'),
                                                         ('Location', 'Location'),
                                                         ('HbA1C', 'HbA1C'),
                                                         ('Gender', 'Gender'),
                                                         ('GI-S', 'GI-S'),
                                                         ('GI-D', 'GI-D'),
                                                         ('DM-type', 'DM-type'),
                                                         ('DM', 'DM'),
                                                         ('CollectionDate', 'CollectionDate'),
                                                         ('Caries Risk', 'Caries Risk'),
                                                         ('BS', 'BS'),
                                                         ('BOP-S', 'BOP-S'),
                                                         ('BOP-D', 'BOP-D'),
                                                         ('Age', 'Age'),
                                                         ('ASA', 'ASA'),
                                                         ('AL-S', 'AL-S'),
                                                         ('AL-D', 'AL-D')
                                                         ], required=True)




class profileInfoForm(forms.Form):
    sampleChoice = forms.ModelMultipleChoiceField(queryset=Sample.objects.all(), required=True)
    taxalevelChoice = forms.ChoiceField(choices=[('rootrank', 'rootrank'),
                                                         ('domain', 'domain'),
                                                         ('phylum', 'phylum'),
                                                         ('class', 'class'),
                                                         ('subclass', 'subclass'),
                                                         ('order', 'order'),
                                                         ('suborder', 'suborder'),
                                                         ('family', 'family'),
                                                         ('genus', 'genus')], required=True)


    methodChoice = forms.ModelChoiceField(queryset=ClassificationMethod.objects.all(), required=True)
    profileVariable = forms.ChoiceField(choices=[('Read Count', 'Read Count'),
                                                         ('Percent of Reads', 'Percent of Reads'),
                                                         ('Average Read Score','Average Read Score')]
                                                , required=True)



class searchbyAttribute (forms.Form):
    attributeChoice = forms.ChoiceField(choices=[('site', 'site'),
                                                         ('run_date', 'run_date'),
                                                         ('patientID', 'patientID'),
                                                         ('depth', 'depth'),
                                                         ('barcode', 'barcode'),
                                                         ('Tooth-S', 'Tooth-S'),
                                                         ('Tooth-D', 'Tooth-D'),
                                                         ('Surf-S', 'Surf-S'),
                                                         ('Surf-D', 'Surf-D'),
                                                         ('Smoke/Pk Yrs', 'Smoke/Pk Yrs'),
                                                         ('Race', 'Race'),
                                                         ('Periodontol Dz DX', 'Periodontol Dz DX'),
                                                         ('PI-S', 'PI-S'),
                                                         ('PI-D', 'PI-D'),
                                                         ('PD-S', 'PD-S'),
                                                         ('PD-D', 'PD-D'),
                                                         ('Mobility-S', 'Mobility-S'),
                                                         ('Mobility-D', 'Mobility-D'),
                                                         ('Location', 'Location'),
                                                         ('HbA1C', 'HbA1C'),
                                                         ('Gender', 'Gender'),
                                                         ('GI-S', 'GI-S'),
                                                         ('GI-D', 'GI-D'),
                                                         ('DM-type', 'DM-type'),
                                                         ('DM', 'DM'),
                                                         ('CollectionDate', 'CollectionDate'),
                                                         ('Caries Risk', 'Caries Risk'),
                                                         ('BS', 'BS'),
                                                         ('BOP-S', 'BOP-S'),
                                                         ('BOP-D', 'BOP-D'),
                                                         ('Age', 'Age'),
                                                         ('ASA', 'ASA'),
                                                         ('AL-S', 'AL-S'),
                                                         ('AL-D', 'AL-D')
                                                         ])
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



