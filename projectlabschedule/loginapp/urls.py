from django.urls import path
from .views import *
urlpatterns = [
    path('',Homepageview.as_view(),name='homepage'),
    path('login/',Loginpageview.as_view(),name='login'),
    path('administrator/',Adminpage.as_view(),name='administrator'),
    path('Student/',Student.as_view(),name='student'),
    path('Staff/',Labstaff.as_view(),name='staff'),
    path('logout/',Logout.as_view(),name='logout'),
    path('Studentreg/',Studentreg.as_view(),name='studentreg'),
    path('Staffreg/',Staffreg.as_view(),name='staffreg'),
    path('adminbase/',AdminBasepage.as_view(),name='adminbase'),
    path('viewstudent/',ViewStudent.as_view(),name='viewstudent'),
    path('viewstaff/',ViewStaff.as_view(),name='viewstaff'),
    

   
]
