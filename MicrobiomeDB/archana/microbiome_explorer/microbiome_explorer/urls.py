from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'microbiome_explorer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),    
    url(r'^$', 'microbiome.views.Home', name = 'Home'),
    url(r'^SampleList$', 'microbiome.views.Sample_list', name = 'Sample'),
    url(r'^ProjectList$', 'microbiome.views.Project_list', name = 'Project'),
)
