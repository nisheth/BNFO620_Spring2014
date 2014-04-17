from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'parikhhi_MicrobiomeProject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'MicrobiomeExplorer.views.home', name="home"),
    url(r'^listProject/', 'MicrobiomeExplorer.views.listProject', name="listProject"),
    url(r'^listSample/', 'MicrobiomeExplorer.views.listSample', name="listSample"),
	
)
