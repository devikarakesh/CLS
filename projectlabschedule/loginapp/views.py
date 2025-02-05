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
from django.shortcuts import render, redirect
from django.views import View
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings


# Forgot Password View
class ForgotPasswordView(View):
    def get(self, request):
        return render(request, 'forgot_password.html')  # HTML form to enter email

    def post(self, request):
        email = request.POST.get('email')
        try:
            user = LoginTable.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            reset_url = f"{request.scheme}://{request.get_host()}/reset-password/{uid}/{token}/"

            # Send reset email
            send_mail(
                'Password Reset Request',
                f'Click the link below to reset your password:\n\n{reset_url}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

            return render(request, 'forgot_password.html', {'message': 'Password reset link sent!'})

        except LoginTable.DoesNotExist:
            return render(request, 'forgot_password.html', {'error': 'Email not found!'})

class ResetPasswordView(View):
    def get(self, request, uid, token):
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = LoginTable.objects.get(id=uid)

            if default_token_generator.check_token(user, token):
                return render(request, 'reset_password.html', {'uid': uid, 'token': token})
            else:
                return render(request, 'reset_password.html', {'error': 'Invalid or expired token'})

        except (LoginTable.DoesNotExist, ValueError):
            return render(request, 'reset_password.html', {'error': 'Invalid request'})

    def post(self, request, uid, token):
        new_password = request.POST.get('password')
        try:
            user = LoginTable.objects.get(id=uid)
            if default_token_generator.check_token(user, token):
                user.password = new_password  # Ideally, hash the password
                user.save()
                return redirect('login')
            else:
                return render(request, 'reset_password.html', {'error': 'Invalid or expired token'})

        except LoginTable.DoesNotExist:
            return render(request, 'reset_password.html', {'error': 'User not found'})