from django.contrib import admin
from MicrobiomeDBApp.models import Project,Sample,SampleVariable,ClassificationMethod

admin.site.register(Project)
admin.site.register(Sample)
admin.site.register(SampleVariable)
admin.site.register(ClassificationMethod)

# Register your models here.
