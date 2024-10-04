
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
    path('viewclass/',Viewclass.as_view(),name='viewclass'), 
    path('updatefaculty/<int:id>/',UpdateFaculty.as_view(),name='updatefaculty'),
    path('Deletefaculty/<int:id>/',DeleteFaculty.as_view(),name='Deletefaculty'),
    path('updatesubjects/<int:id>/',Updatesubjects.as_view(),name='updatesubjects'),
    path('Deletesubjects/<int:id>/',Deletesubjects.as_view(),name='Deletesubjects'),
    path('updateclass/<int:id>/',UpdateClass.as_view(),name='updateclass'),
    path('Deleteclass/<int:id>/',Deleteclass.as_view(),name='Deleteclass'),
]
