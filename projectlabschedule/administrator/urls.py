"""
URL configuration for projectlabschedule project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import *

urlpatterns = [
    path('addnotification/',notification.as_view(),name='notification'),
    path('updatenotification/<int:id>/',Updatenotification.as_view(),name='updatenotification'),
    path('Deletenotification/<int:id>/',Deletenotification.as_view(),name='Deletenotification'),
    path('addfaculty/',Addfaculty.as_view(),name='addfaculty'),    
    path('viewfaculty/',Viewfaculty.as_view(),name='viewfaculty'),  
    path('Generate/',GenerateTTbutton.as_view(),name='Generate'),
    path('viewsubjects/',Viewsubjects.as_view(),name='viewsubjects'), 
    path('addsubjects/',Addsubjects.as_view(),name='addsubjects'), 
    path('addclass/',Addclass.as_view(),name='addclass'), 
]
