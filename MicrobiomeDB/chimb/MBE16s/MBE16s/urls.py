from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'MBE16s.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
   # url(r'^$', 'OralMBE.views.home', name='home'),
   # url(r'^projects$', 'OralMBE.views.projects', name='projects'),
    #url(r'^samples$', 'OralMBE.views.samples', name='samples'),
)
