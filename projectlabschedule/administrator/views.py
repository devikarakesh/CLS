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

class Addfaculty(View):
    def get(self,request):
        return render(request,'admin/addfaculty.html')
    def post(self,request):
        form=Addfacultyform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('viewfaculty')

class Viewfaculty(View):
    def get(self,request):
        f=Faculty1.objects.all()
        return render(request,'admin/viewfaculty.html',{'faculties':f})

class GenerateTTbutton(View):
    def get(self,request):
        return render(request,'admin/GenerateTTbuttons.html')

class Viewsubjects(View):
    def get(self,request):
        s=Subject1.objects.all()
        return render(request,'admin/viewsubjects.html',{'subjects':s})


class Addsubjects(View):
    def get(self,request):
        c=Faculty1.objects.all()
        return render(request,'admin/addsubject.html',{'faculties':c})
        
    def post(self,request):
        form=Addsubjectform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('viewsubjects')

class Addclass(View):
    def get(self,request):
        o=Subject1.objects.all()
        return render(request,'admin/addclass.html',{'subjects':o})
        
    def post(self,request):
        form=Addclassform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('viewclass')

class Viewclass(View):
    def get(self,request):
        c=Class1.objects.all()
        return render(request,'admin/viewclass.html',{'C':c})

class UpdateFaculty(View):
    def get(self,request,id):
        n=Faculty1.objects.get(id=id)
        return render(request,'admin/updatefaculty.html',{'n':n})
    def post(self,request,id):
        n=Faculty1.objects.get(id=id)
        form=Updatefacultyform(request.POST,instance=n)
        if form.is_valid():
            form.save()
            return redirect('viewfaculty')


class DeleteFaculty(View):
    def get(self,request,id):
        n=Faculty1.objects.get(id=id)
        n.delete()
        return redirect('viewfaculty')

class Updatesubjects(View):
    def get(self,request,id):
        s=Subject1.objects.get(id=id)
        n=Faculty1.objects.all()
        return render(request,'admin/updatesubjects.html',{'s':s,'faculties':n})
    def post(self,request,id):
        s=Subject1.objects.get(id=id)
        form=Updatesubjectsform(request.POST,instance=s)
        if form.is_valid():
            form.save()
            return redirect('viewsubjects')

class Deletesubjects(View):
    def get(self,request,id):
        s=Subject1.objects.get(id=id)
        s.delete()
        return redirect('viewsubjects')


class UpdateClass(View):
    def get(self,request,id):
        o=Class1.objects.get(id=id)
        return render(request,'admin/updateclass.html',{'o':o})
    def post(self,request,id):
        o=Class1.objects.get(id=id)
        form=UpdateClassform(request.POST,instance=o)
        if form.is_valid():
            form.save()
            return redirect('viewclass')

class Deleteclass(View):
    def get(self,request,id):
        s=Class1.objects.get(id=id)
        s.delete()
        return redirect('viewclass')
