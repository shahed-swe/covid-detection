from django.urls import path
from django.conf.urls import include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('detectchest/', views.detectchest, name='detectchest'),
    path('register/', views.myregistration, name='myregistration'),
    path('login/', views.mylogin, name='mylogin'),
    path('logout/', views.mylogout, name='mylogout'),
    path('reports/', views.ReportViewSet.as_view(), name='reports'),
    path('reportgraph/', views.show_report_graph, name="show_report_graph"),
]