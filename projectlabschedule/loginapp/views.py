from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth import authenticate
from .models import Userprofile,Token
from django.contrib import messages
import json
from administrator.models import notifications

from administrator.forms import AddStudentform
from .models import *
from django.http import HttpResponse


# Create your views here.

class Homepageview(View):
 def get(self,request):
  n=notifications.objects.all()
  return render(request,'mainhome.html',{'n':n})
 
class Loginpageview(View):
  def get(self,request):
   return render(request,'mlog1.html')
  def post(self,request):
    user_type=""
    response_dict={"success":False}
    landing_page_url={
      "ADMIN":"administrator",
      "FACULTY":"faculty",
      "STUDENT":"student",
      "LABSTAFF":"staff"
    }
    username=request.POST.get("username")
    password=request.POST.get("password")
    print(username)
    authenticated=authenticate(username=username,password=password)
    try:
      user=Userprofile.objects.get(username=username)
      print("hel")
    except Userprofile.DoesNotexist:
      response_dict[
        "reason"
      ]="No account found fpr this username.Please signup"
      messages.error(request,response_dict["reason"])
    if not authenticated:
        response_dict["reason"]="Invalid credentials"
        messages.error(request,response_dict["reason"])
        return redirect(request.GET.get("from")or "user:login")
    else:
      print("hello")
      session_dict={"real_user":authenticated.id}
      token,c=Token.objects.get_or_create(
        user=user,defaults={"session_dict":json.dumps(session_dict)}
      )
      user_type=authenticated.user_type
      request.session['user_id']=authenticated.id
      print("hai")
      print(user)
      print(user_type)
      return redirect(landing_page_url[user_type])
    return redirect(request.GET.get("from") or  loadlogin)
      
    
  
 
class Adminpage(View):
 def get(self,request):
  return render(request,'admin/admin.html')


class Labstaff(View):
  def get(self,request):
   return render(request,'staff/staffdashboard.html')

class Faculty(View):
  def get(self,request):
    return render(request,'faculty/facultydashboard.html')
  



class Student(View):
 def get(self,request):
  return render(request,'student/studentdashboard.html')
 





class AdminBasepage(View):
 def get(self,request):
  return render(request,'admin/adminbase.html')
 


  


class Addnotifications(View):
  def get(self,request):
    return render(request,'admin/addnotification.html')



class Logout(View):
    def get(self,request):
        request.session["token"]=None
        request.session.flush()
        return redirect("login")