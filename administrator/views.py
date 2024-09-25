from django.shortcuts import render,redirect
from django.views import View
from .forms import *


# Create your views here.
class notification(View):
    def get(self,request):
        return render(request,'addnotidication.html')
    def post(self,request):
        form=Addnotificationform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('viewnotifications')

class Updatenotification(View):
    def get(self,request,id):
        n=notifications.objects.get(id=id)
        return render(request,'admin/updatenotification.html',{'n':n})
    def post(self,request,id):
        n=notifications.objects.get(id=id)
        form=Updatenotificationform(request.POST,instance=n)
        if form.is_valid():
            form.save()
            return redirect('viewnotifications')
class Deletenotification(View):
    def get(self,request,id):
        n=notifications.objects.get(id=id)
        n.delete()
        return redirect('viewnotifications')


