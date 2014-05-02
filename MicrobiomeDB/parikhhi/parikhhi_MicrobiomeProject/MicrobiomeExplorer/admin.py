# Register your models here.

from django.contrib import admin
from MicrobiomeExplorer.models import Project
from MicrobiomeExplorer.models import Sample
from MicrobiomeExplorer.models import SampleVariable
from MicrobiomeExplorer.models import Read
from MicrobiomeExplorer.models import ClassificationMethod
from MicrobiomeExplorer.models import TaxaID
from MicrobiomeExplorer.models import ReadAssignment
from MicrobiomeExplorer.models import ProfileSummary


admin.site.register(Project)
admin.site.register(Sample)
admin.site.register(SampleVariable)
admin.site.register(Read)
admin.site.register(ClassificationMethod)
admin.site.register(TaxaID)
admin.site.register(ReadAssignment)
admin.site.register(ProfileSummary)


