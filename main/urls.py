from django.urls import path
from django.conf.urls import include,url
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('doctor/', views.doctorhome, name="doctorhome"),
    url(r'^condition/(?P<id>.*)/$', views.patientcondition, name="patientcondition"),
    path('detectchest/', views.detectchest, name='detectchest'),
    path('register/', views.myregistration, name='myregistration'),
    path('doctorregistration/', views.doctorregistration, name="doctorregistration"),
    path('login/', views.mylogin, name='mylogin'),
    path('logout/', views.mylogout, name='mylogout'),
    path('reports/', views.ReportViewSet.as_view(), name='reports'),
    path('reportgraph/', views.show_report_graph, name="show_report_graph"),
    path('covid_test',views.covid_symtoms_check, name="covid_symtoms_check")

    
]
