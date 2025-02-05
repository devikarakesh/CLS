from django.urls import path
from .views import *
urlpatterns = [
    path('',Homepageview.as_view(),name='homepage'),
    path('login/',Loginpageview.as_view(),name='login'),

    path('administrator/',Adminpage.as_view(),name='administrator'),

    
    

    path('Faculty/',Faculty.as_view(),name='faculty'),

    path('logout/',Logout.as_view(),name='logout'),

    path('adminbase/',AdminBasepage.as_view(),name='adminbase'),
    
    path('Student/',Student.as_view(),name='student'),
    

    path('Staff/',Labstaff.as_view(),name='staff'),
    


    path('Addnotifications/',Addnotifications.as_view(),name='Addnotifications'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/<uid>/<token>/', ResetPasswordView.as_view(), name='reset_password'),

   
]
