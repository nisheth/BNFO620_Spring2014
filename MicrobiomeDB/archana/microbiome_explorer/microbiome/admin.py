from django.contrib import admin

from microbiome.models import Project
from microbiome.models import Sample
from microbiome.models import SampleVariable
from microbiome.models import Read
from microbiome.models import Method
from microbiome.models import Taxonomy
from microbiome.models import ReadAssignment
from microbiome.models import ProfileSummary


admin.site.register(Project)
admin.site.register(Sample)
admin.site.register(SampleVariable)
admin.site.register(Read)
admin.site.register(Method)
admin.site.register(Taxonomy)
admin.site.register(ReadAssignment)
admin.site.register(ProfileSummary)
