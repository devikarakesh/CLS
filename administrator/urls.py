
from django.urls import path
from .views import *

urlpatterns = [
    path('addnotification/',notification.as_view(),name='notification'),
    path('updatenotification/<int:id>/',Updatenotification.as_view(),name='updatenotification'),
    path('Deletenotification/<int:id>/',Deletenotification.as_view(),name='Deletenotification'),
    path('viewnotifications/',Viewnotifications.as_view(),name='viewnotifications'),


    
    path('Generate/',GenerateTTbutton.as_view(),name='Generate'),
    
    path('viewsubjects/',Viewsubjects.as_view(),name='viewsubjects'), 
    path('addsubjects/',Addsubjects.as_view(),name='addsubjects'), 
    path('addclass/',Addclass.as_view(),name='addclass'), 
    path('viewclass/',Viewclass.as_view(),name='viewclass'), 

    path('addfaculty/',Addfaculty.as_view(),name='addfaculty'),    
    path('viewfaculty/',Viewfaculty.as_view(),name='viewfaculty'),
    path('updatefaculty/<int:id>',UpdateFaculty.as_view(),name='updatefaculty'),
    path('Deletefaculty/<int:id>',DeleteFaculty.as_view(),name='Deletefaculty'),

    path('updatesubjects/<int:id>',Updatesubjects.as_view(),name='updatesubjects'),
    path('Deletesubjects/<int:id>',Deletesubjects.as_view(),name='Deletesubjects'),

    path('updateclass/<int:id>/',UpdateClass.as_view(),name='updateclass'),
    path('Deleteclass/<int:id>/',Deleteclass.as_view(),name='Deleteclass'),

    path ('Generatetimetable/', generate_timetable,name='Generate timetable'),
    path('viewtimetable/',TimetableView1.as_view(),name='viewtimetable'),


    path('Addlabs/',AddLab.as_view(),name='lab_list'),
    path('Editlab/<int:pk>/',Editlab.as_view(),name='lab_detail'),
    path('Deletelab/<int:pk>/',LabDeleteView.as_view(),name='lab_delete'),
    path('ViewAddedlabs/',ViewAddedlabs.as_view(),name='ViewAddedlabs'),
    path('viewlabs/',ViewLabs.as_view(),name='viewlabs'),

    path('viewworkingday/<int:id>/',Viewworkingday.as_view(),name='viewworkingday'),
    path('addworkingday/<int:id>/',Addworkingday.as_view(),name='addwworkingday'),
    path('editworkingday/<int:id>/',Editworkingday.as_view(),name='editworkingday'),
    path('Deleteworkingday/<int:id>/',Deleteworkingday.as_view(),name='deleteworkingday'),

    path('viewtimeslot/<int:id>',Viewtimeslot.as_view(),name='viewtimeslot'),
    path('addtimeslot/<int:id>',Addtimeslot.as_view(),name='addtimeslot'),
    path('edittimeslot/<int:id>/',Edittimeslot.as_view(),name='editworkingday'),
    path('Deletetimeslot/<int:id>/',Deletetimeslot.as_view(),name='deleteworkingday'),

    path('staffdashboard/',Staffdashboard.as_view(),name='staffdashboard'),
    path('staffviewnotification/',StaffViewnotifications.as_view(),name='staffviewnotification'),
    path('addnotificationbystaff/',notificationbystaff.as_view(),name='addnotificationbystaff'),
    path('updatenotificationbystaff/<int:id>/',Updatenotificationbystaff.as_view(),name='updatenotificationbystaff'),
    path('Deletenotificationbysatff/<int:id>/',Deletenotificationbystaff.as_view(),name='Deletenotificationbystaff'),

    # path('updatestudent/<int:id>/',Updatestudent.as_view(),name='updatestudent'),
    path('viewtimetablebystaff/',TimetableView2.as_view(),name='viewtimetablebystaff'),
    path('viewnotificationsbystaff/',Viewnotificationsaddedbystaff.as_view(),name='viewnotificationsbystaff'),
    path('viewtimetablebyfaculty/',TimetableView3.as_view(),name='viewtimetablebyfaculty'),
    path('editprofilebyfaculty/<int:id>/',Editprofilebyfaculty.as_view(),name='editprofilebyfaculty'),

    path('viewstudent/',ViewStudent.as_view(),name='viewstudent'),
    path('Studentreg/',Studentreg.as_view(),name='studentreg'),

    # path('viewstaff/',ViewStaff.as_view(),name='viewstaff'),
    # path('Staffreg/',Staffreg.as_view(),name='staffreg'),


    path('updatestudent/<int:id>',Updatestudent.as_view(),name='updatestudent'),
    path('Deletestudent/<int:id>',Deletestudent.as_view(),name='Deletestudent'),


    path('lab/<int:lab_id>/book/', LabBookingView.as_view(), name='lab_booking'),
    path('adminlab/<int:lab_id>/book/', AdminLabBookingView.as_view(), name='adminlab_booking'),
   
    path('booking/<int:booking_id>/confirmation/', BookingConfirmationView.as_view(), name='booking_confirmation'),
    path('booking/<int:booking_id>/edit/', EditBookingView.as_view(), name='edit_booking'),
    path('booking/<int:booking_id>/delete/', DeleteBookingView.as_view(), name='delete_booking'),

    path('FacultyViewAddedlabs/',FacultyViewAddedlabs.as_view(),name='FacultyViewAddedlabs'),
    path('Flab/<int:lab_id>/book/', FacultyLabBookingView.as_view(), name='FacultyLabBookingView'),

    path('Regbuttons/',regButton.as_view(),name='Regbuttons'),
    path('addfaculty/',Addfaculty.as_view(),name='addfaculty'),   

    





]
