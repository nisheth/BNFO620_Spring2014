from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'MicrobiomeDB.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$','MicrobiomeDBApp.views.home'),
    url(r'^projects','MicrobiomeDBApp.views.projects', name='projects'),
    url(r'^samples','MicrobiomeDBApp.views.samples', name='samples'),
)
