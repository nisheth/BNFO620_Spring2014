from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'MicrobiomeDB.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$','MicrobiomeSnehalApp.views.home'),
    url(r'^projects','MicrobiomeSnehalApp.views.projects', name='projects'),
    url(r'^showInfo','MicrobiomeSnehalApp.views.showInfo', name='showInfo'),
    url(r'^showProfile', 'MicrobiomeSnehalApp.views.showProfile', name='showProfile'),
    url(r'^sample', 'MicrobiomeSnehalApp.views.samples', name = 'sample'),
    url(r'^searchVariable', 'MicrobiomeSnehalApp.views.variablesearch', name = 'variablesearch'),
    url(r'^searchProfile', 'MicrobiomeSnehalApp.views.profileSearch', name = 'searchProfile'),
    #url(r'^showProfile','MicrobiomeSnehalApp.views.showProfile', name='showProfile'),
)
