from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^signup$',views.signup, name='signup'),
    url(r'^department/(?P<name>[a-zA-Z]+)$',views.departmentview, name='department'),
    # url(r'^search$',views.search, name='search'),
    url(r'^profile/(?P<username>[a-zA-Z0-9_.]+)$', views.profile, name='profile'),
    url(r'^profile/(?P<username>[a-zA-Z0-9_.]+)/edit$', views.profileedit, name='profileedit'),
    # url(r'^profile/(?P<username>[a-zA-Z0-9_.]+)/students$', views.studentsview, name='students'),
    # url(r'^profile/(?P<username>[a-zA-Z0-9_.]+)/students/add$', views.studentadd, name='studentadd'),
    # url(r'^profile/(?P<username>[a-zA-Z0-9_.]+)/students/delete$',views.studentdel, name='studentdelete'),
    # url(r'^profile/(?P<username>[a-zA-Z0-9_.]+)/teachings$', views.teachingview, name='teachings'),
    # url(r'^profile/(?P<username>[a-zA-Z0-9_.]+)/teaching/add$', views.teachingadd, name='teachingadd'),
    # url(r'^profile/(?P<username>[a-zA-Z0-9_.]+)/teaching/delete$', views.teachingdel, name='teachingdelete'),
    url(r'^profile/(?P<username>[a-zA-Z0-9_.]+)/projects$', views.projectsview, name='projects'),
    url(r'^profile/(?P<username>[a-zA-Z0-9_.]+)/projects/add$', views.projectadd, name='projectadd'),
    url(r'^profile/(?P<username>[a-zA-Z0-9_.]+)/projects/delete$', views.projectdel, name='projectdelete'),
    url(r'^profile/(?P<username>[a-zA-Z0-9_.]+)/publications$', views.publicationsview, name='publications'),
    url(r'^profile/(?P<username>[a-zA-Z0-9_.]+)/publications/add$', views.publicationadd, name='publicationadd'),
    url(r'^profile/(?P<username>[a-zA-Z0-9_.]+)/publications/delete$', views.publicationdel, name='publicationdelete'),
    url(r'^profile/(?P<username>[a-zA-Z0-9_.]+)/recognitions$', views.recognitionsview, name='recognitions'),
    url(r'^profile/(?P<username>[a-zA-Z0-9_.]+)/recognitions/add$', views.recognitionadd, name='recognitionadd'),
    url(r'^profile/(?P<username>[a-zA-Z0-9_.]+)/recognitions/delete$', views.recognitiondel, name='recognitiondelete'),
    url(r'^profile/(?P<username>[a-zA-Z0-9_.]+)/experiences$', views.experiencesview, name='experiences'),
    url(r'^profile/(?P<username>[a-zA-Z0-9_.]+)/experiences/add$', views.experienceadd, name='experienceadd'),
    url(r'^profile/(?P<username>[a-zA-Z0-9_.]+)/experiences/delete$', views.experiencedel, name='experiencedelete')
]