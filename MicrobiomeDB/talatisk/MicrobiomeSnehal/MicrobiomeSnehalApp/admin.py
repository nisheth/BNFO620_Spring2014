from django.contrib import admin
from MicrobiomeSnehalApp.models import Project,Sample,SampleVariable,ClassificationMethod,TaxaTable, ProfileSummary

admin.site.register(Project)
admin.site.register(Sample)
admin.site.register(SampleVariable)
admin.site.register(ClassificationMethod)
admin.site.register(TaxaTable)
admin.site.register(ProfileSummary)

# Register your models here.
