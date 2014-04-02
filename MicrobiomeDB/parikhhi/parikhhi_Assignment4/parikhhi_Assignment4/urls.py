from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'parikhhi_Assignment4.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

	url(r'^admin/', include(admin.site.urls)),
	url(r'^$', 'stufacultyinfosys.views.home', name="home"),
	url(r'^login', 'stufacultyinfosys.views.login', name="login"),
	url(r'^logout', 'stufacultyinfosys.views.logout', name="logout"),
	url(r'^register/', 'stufacultyinfosys.views.register', name="register"),
	url(r'^facultyhome/', 'stufacultyinfosys.views.facultyhome', name="facultyhome"),
	url(r'^addmajor/', 'stufacultyinfosys.views.addMajor', name="addMajor"),
	url(r'^addcourse/', 'stufacultyinfosys.views.addCourse', name="addCourse"),
	url(r'^studenthome/', 'stufacultyinfosys.views.studenthome', name="studenthome"),
	url(r'^registercourse/', 'stufacultyinfosys.views.registercourse', name="registercourse"),
	url(r'^listhome/', 'stufacultyinfosys.views.listhome', name="listhome"),
	url(r'^listfaculty/', 'stufacultyinfosys.views.listfaculty', name="listfaculty"),
	url(r'^liststudent/', 'stufacultyinfosys.views.liststudent', name="liststudent"),
	url(r'^listcourse/', 'stufacultyinfosys.views.listcourse', name="listcourse"),
	url(r'^accounts/login/$', 'django.contrib.auth.views.login',{'template_name': 'login.html'}),

)
