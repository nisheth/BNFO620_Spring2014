from django.contrib import admin
from OralMBE.models import Project
from OralMBE.models import Sample
from OralMBE.models import SampleAttribute
from OralMBE.models import ClassificationMethod
from OralMBE.models import Taxa
from OralMBE.models import ProfileSummary


# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    search_fields = ['name']
    fieldsets = [
        ('name', {'fields':['name']}),
        ('description', {'fields':['description']}),
        ('contactname', {'fields':['contactname']}),
        ('contactemail', {'fields':['contactemail']}),
        ]
    list_display = ['name', 'description', 'contactname', 'contactemail']
    list_filter = ['name', 'description', 'contactname', 'contactemail']

class SampleAdmin(admin.ModelAdmin):
    search_fields = ['name']
    fieldsets = [
        ('project', {'fields':['project']}),
        ('name', {'fields':['name']}),

        ]
    list_display = ['project','name']
    list_filter = ['project','name']

class SampleAttributeAdmin(admin.ModelAdmin):
    search_fields = ['sample','attribute','value']
    fieldsets = [
        ('sample', {'fields':['sample']}),
        ('attribute', {'fields':['attribute']}),
        ('value', {'fields':['value']})
        ]
    list_display = ['sample','attribute','value']
    list_filter = ['sample','attribute','value']

class ClassificationMethodAdmin(admin.ModelAdmin):
    search_fields = ['key','description']
    fieldsets = [
        ('key', {'fields':['key']}),
        ('description', {'fields':['description']}),
        ('contactname', {'fields':['contactname']}),
        ('contactemail', {'fields':['contactemail']}),
        ]
    list_display = ['key', 'description', 'contactname', 'contactemail']
    list_filter = ['key', 'description', 'contactname', 'contactemail']

class TaxaAdmin(admin.ModelAdmin):
    search_fields = ['name','level']
    fieldsets = [
        ('name', {'fields':['name']}),
        ('level', {'fields':['level']})
        ]
    list_display = ['name', 'level']
    list_filter = ['name', 'level']

#class ProfileSummaryAdmin(admin.ModelAdmin):
   # search_fields = ['sample','classificationmethod','taxa','numreads','perctotal','avgscore']
   # fieldsets = [
   #     ('sample', {'fields':['sample']}),
   #     ('classificationmethod', {'fields':['classificationmethod']}),
   #     ('taxa', {'fields':['taxa']}),
   #     ('numreads', {'fields':['numreads']}),
    #    ('perctotal', {'fields':['perctotal']}),
   #     ('avgscore', {'fields':['avgscore']})
    #    ]
    #list_display = ['sample','classificationmethod','taxa','numreads','perctotal','avgscore']
    #list_filter = ['sample','classificationmethod','taxa','numreads','perctotal','avgscore']


admin.site.register(Project, ProjectAdmin)

admin.site.register(Sample, SampleAdmin)

admin.site.register(SampleAttribute, SampleAttributeAdmin)

admin.site.register(ClassificationMethod, ClassificationMethodAdmin)

admin.site.register(Taxa, TaxaAdmin)
admin.site.register(ProfileSummary)