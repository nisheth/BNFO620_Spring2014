from django.contrib import admin
from OralMBE.models import Project
from OralMBE.models import Sample
from OralMBE.models import SampleAttribute
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

admin.site.register(Project, ProjectAdmin)

admin.site.register(Sample, SampleAdmin)

admin.site.register(SampleAttribute, SampleAttributeAdmin)

