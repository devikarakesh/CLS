from django.shortcuts import render,redirect
from django.views import View
from .forms import *
from django.urls import reverse


# Create your views here.
class notification(View):
    def get(self,request):
        return render(request,'admin/addnotification.html')
    def post(self,request):
        form=Addnotificationform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('viewnotifications')

class Updatenotification(View):
    def get(self,request,id):
        n=notifications.objects.get(id=id)
        return render(request,'admin/updatenotification.html',{'notificationobject':n})
    def post(self,request,id):
        n=notifications.objects.get(id=id)
        form=Updatenotificationform(request.POST,instance=n)
        if form.is_valid():
            form.save()
            return redirect('viewnotifications')
        else:
            print(form.errors) 


class Deletenotification(View):
    def get(self,request,id):
        n=notifications.objects.get(id=id)
        n.delete()
        return redirect('viewnotifications')

class Viewnotifications(View):
  def get(self,request):
    notificationobject=notifications.objects.all()
    return render(request,'admin/viewnotifications.html',{'notificationobject':notificationobject})

class Viewfaculty(View):
    def get(self,request):
        f=Faculty1.objects.all()
        return render(request,'admin/viewfaculty.html',{'faculties':f})

class Addfaculty(View):
    def get(self,request):
        return render(request,'admin/addfaculty.html')
    def post(self,request):
        form=Addfacultyform(request.POST)
    
        if form.is_valid():
            reg_form=form.save(commit=False)
            login_instance=Userprofile.objects.create_user(username=request.POST['username'],password=request.POST['password'],user_type='FACULTY')
            reg_form.loginid=login_instance
            reg_form.save()
            form.save()
            return redirect('viewfaculty')

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
        c = Class1.objects.prefetch_related('subjects').all()
        print(c)
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
        subjects=Subject1.objects.all()
        print(subjects)
        print(o)
        return render(request,'admin/updateclass.html',{'o':o,'subjects':subjects})
    def post(self,request,id):
        o = Class1.objects.get(id=id)
        o.Semester = request.POST.get('Semester')
        o.save()
        # Update the ManyToManyField (subjects)
        selected_subjects = request.POST.getlist('subjects')  # Get selected subject IDs
        o.subjects.set(selected_subjects)  # Update the ManyToManyField
        return redirect('viewclass')

class Deleteclass(View):
    def get(self,request,id):
        s=Class1.objects.get(id=id)
        s.delete()
        return redirect('viewclass')

from django.http import HttpResponse
from django.db.models import Count
from .models import Class1, Subject1, TimetableEntry1
import random
from random import shuffle
from django.views import View
def generate_timetable(request):
    #delete all timetable entries
    TimetableEntry1.objects.all().delete()
    # Get all classes
    classes = Class1.objects.all()
    
    # Define the days and periods
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    periods = [1, 2, 3, 4, 5]  # Assuming 5 periods per day
    
    # Identify common subjects across all classes
    common_subject_ids = Subject1.objects.annotate(class_count=Count('class1')).filter(class_count__gt=1).values_list('id', flat=True)
    common_subjects = Subject1.objects.filter(id__in=common_subject_ids)
    uncommon_subjects = Subject1.objects.exclude(id__in=common_subject_ids)
    common_subject_slots = {}
    selected_slots=[]

    # Assign common subjects
    for subject in common_subjects:
        # Collect available slots across all classes where the subject is taught
        available_slots = []
        for cls in classes:
            class_subjects = cls.subjects.all()
            if subject in class_subjects:
                for day in days:
                    for period in periods:
                        available_slots.append({
                            'day': day,
                            'period': period,
                            'cls': cls
                        })

        # Assign slots for the subject
        
        hours_remaining = subject.contact_hours

        if available_slots:
            num_slots_to_select = min(len(available_slots), hours_remaining)
            selected_slots = random.sample(available_slots, num_slots_to_select)
        else:
            print(f"No available slots for subject {subject.name}")
            selected_slots = []  # Ensure selected_slots is defined

        # Save selected slots for the subject
        common_subject_slots[subject.id] = selected_slots
        
    # Initialize timetable for each class
    for cls in classes:
        # Get subjects for the class
        class_subjects = cls.subjects.all()
        
        # Initialize timetable
        timetable = []
        for day in days:
            for period in periods:
                timetable.append({
                    'day': day,
                    'period': period,
                    'cls': cls,
                    'subject': None
                })
        
        # Assign common subjects
        for subject_id, slots in common_subject_slots.items():
            subject = Subject1.objects.get(id=subject_id)
            if subject in class_subjects:
                for slot in slots:
                    # Ensure that the slot is available
                    while True:
                        if not TimetableEntry1.objects.filter(day=slot['day'], period=slot['period'], cls=cls, subject=subject).exists():
                            TimetableEntry1.objects.create(
                                day=slot['day'],
                                period=slot['period'],
                                cls=cls,
                                subject=subject,
                                faculty=subject.faculty
                            )
                            print(f"Assigned {subject.name} to {cls.name} on {slot['day']} period {slot['period']}")
                            break  # Exit loop when assignment is successful
                        else:
                            # print(f"Slot already occupied: {slot['day']} period {slot['period']} for {subject.name} in {cls.name}")
                            # Remove the occupied slot and try another one
                            slots.remove(slot)
                            if slots:
                                slot = random.choice(slots)
                            else:
                                print(f"No more available slots for {subject.name} in {cls.name}")
                                break  # Exit loop if no slots are available
        
    empty_slots = []
    # Calculate empty slots by filtering out occupied ones from the timetable
    for cls in classes:
        # Get all periods for this class
        timetable_entries = TimetableEntry1.objects.filter(cls=cls)

        # Initialize a list of all possible slots for this class
        full_slots = []
        for day in days:
            for period in periods:
                full_slots.append({'day': day, 'period': period, 'cls': cls})

        # Filter out the slots already occupied in the timetable
        
        for slot in full_slots:
            if not timetable_entries.filter(
                day=slot['day'], 
                period=slot['period'],
                cls=slot['cls']
            ).exists():
                empty_slots.append(slot)
    print('emptyslots',empty_slots)
 
        # Create a dictionary to store subjects by the same faculty across all classes
    faculty_subjects = {}

    # Loop through all classes
    for cls in Class1.objects.all():
        class_subjects = cls.subjects.all()  # Get all subjects for this class

        for subject in uncommon_subjects:
            faculty = subject.faculty
            
            # Check if this faculty is already in the dictionary
            if faculty not in faculty_subjects:
                faculty_subjects[faculty] = set()  # Initialize an empty set for subjects
            
            # Add the full subject object to the faculty's set of subjects
            faculty_subjects[faculty].add(subject)

    # Filter only faculty who teach multiple subjects
    faculty_multiple_subjects = {faculty: subjects for faculty, subjects in faculty_subjects.items() if len(subjects) > 1}

    # Print final result (optional)
    # print(faculty_multiple_subjects)

    # First Pass: Assign subjects without checking if the faculty is already occupied
    for faculty, subjects in faculty_multiple_subjects.items():
        # Process each subject for the faculty
        for subject in subjects:
            # Only assign the subject if it belongs to the class for the current empty slot
            # print('Subject:', subject)

            # Loop through each class
            for cls in Class1.objects.all():
                # print('Class:', cls.id)
                
                if subject in cls.subjects.all():  # Ensure subject is part of the current class
                    hours_remaining = subject.contact_hours
                    # print('Hours remaining:', hours_remaining)
                    # print('Contact hours:', subject.contact_hours)

                    # Collect available slots for this class
                    available_slots = [entry for entry in empty_slots if entry['cls'].id == cls.id]
                    # print('Available slots:', available_slots)
                    # Shuffle to get a random order
                    shuffle(available_slots)
                    
                    # Assign slots
                    for entry in available_slots:
                        if hours_remaining <= 0:
                            break
                        # Ensure the slot is available and not already occupied
                        if not TimetableEntry1.objects.filter(day=entry['day'], period=entry['period'], cls=cls, subject=subject).exists():
                            # Initially, we skip the check for faculty conflict
                            TimetableEntry1.objects.create(
                                day=entry['day'],
                                period=entry['period'],
                                cls=entry['cls'],
                                subject=subject,
                                faculty=faculty
                            )
                            hours_remaining -= 1
                            # print('Hours remaining after assignment:', hours_remaining)
                            empty_slots.remove(entry)
                            if hours_remaining == 0:
                                break  # Exit loop when all hours are assigned
                        else:
                            print(f"Slot already occupied for subject {subject.name} in class {cls.name} on {entry['day']} period {entry['period']}")
                    
                    # If the subject is not assigned yet and there are no available slots left, print a message
                    if hours_remaining > 0:
                        print(f"No available slots for {subject.name} in class {cls.name}")
    empty_slots = []
    # Calculate empty slots by filtering out occupied ones from the timetable
    for cls in classes:
        # Get all periods for this class
        timetable_entries = TimetableEntry1.objects.filter(cls=cls)

        # Initialize a list of all possible slots for this class
        full_slots = []
        for day in days:
            for period in periods:
                full_slots.append({'day': day, 'period': period, 'cls': cls})

        # Filter out the slots already occupied in the timetable
        
        for slot in full_slots:
            if not timetable_entries.filter(
                day=slot['day'], 
                period=slot['period'],
                cls=slot['cls']
            ).exists():
                empty_slots.append(slot)
    print('emptyslots',empty_slots)
    
    
    # Second Pass: Check for faculty conflicts and reassign if necessary
    for faculty in faculty_multiple_subjects.keys():
        # Find all timetable entries for this faculty
        faculty_entries = TimetableEntry1.objects.filter(faculty=faculty)
        
        # Dictionary to track periods and days where the faculty is already scheduled
        occupied_slots = {}
        
        # Loop through each entry for this faculty
        for entry in faculty_entries:
            slot_key = (entry.day, entry.period)
            
            if slot_key in occupied_slots:
                # Conflict found: faculty is already assigned in this slot
                conflicting_entry = occupied_slots[slot_key]
                # print(f"Conflict found: faculty {faculty} is scheduled for both {conflicting_entry.subject.name} and {entry.subject.name} on {entry.day}, period {entry.period}.")
                
                # Try to reassign one of the subjects (you can choose which one to reassign)
                reassign_entry = entry  # For example, reassign the current entry
                reassign_cls = reassign_entry.cls
                reassign_subject = reassign_entry.subject
                
                # Collect available slots for reassignment
                available_slots = [e for e in empty_slots if e['cls'] == reassign_cls]
                shuffle(available_slots)
                
                # Find a new slot for the conflicting subject
                for new_entry in available_slots:
                    if not TimetableEntry1.objects.filter(day=new_entry['day'], period=new_entry['period'], faculty=faculty).exists():
                        # Reassign to a new slot
                        TimetableEntry1.objects.filter(id=reassign_entry.id).update(
                            day=new_entry['day'],
                            period=new_entry['period']
                        )
                        # print(f"Reassigned subject {reassign_subject.name} to {new_entry['day']} period {new_entry['period']} for class {reassign_cls.name}.")
                        empty_slots.remove(new_entry)
                        break
            else:
                # No conflict, mark the slot as occupied by this faculty
                occupied_slots[slot_key] = entry

    # Flatten the list of subjects from faculty_multiple_subjects
    faculty_subject_ids = [subject.id for subjects in faculty_multiple_subjects.values() for subject in subjects]

    # Identify remaining subjects by excluding subjects from faculty_multiple_subjects
    remaining_subjects = uncommon_subjects.exclude(id__in=faculty_subject_ids)
    print('remaining_subjects',remaining_subjects)
    
    empty_slots = []
    # Calculate empty slots by filtering out occupied ones from the timetable
    for cls in classes:
        # Get all periods for this class
        timetable_entries = TimetableEntry1.objects.filter(cls=cls)

        # Initialize a list of all possible slots for this class
        full_slots = []
        for day in days:
            for period in periods:
                full_slots.append({'day': day, 'period': period, 'cls': cls})

        # Filter out the slots already occupied in the timetable
        
        for slot in full_slots:
            if not timetable_entries.filter(
                day=slot['day'], 
                period=slot['period'],
                cls=slot['cls']
            ).exists():
                empty_slots.append(slot)
    print('emptyslots',empty_slots)
    

    for cls in Class1.objects.all():
        class_subjects = cls.subjects.all()  # Get all subjects for this class

        for subject in remaining_subjects:
            if subject in class_subjects:  # Only assign if the subject is in the current class
                hours_remaining = subject.contact_hours

                # Collect available slots for this class
                available_slots = [entry for entry in empty_slots if entry['cls'].id == cls.id]
                shuffle(available_slots)  # Shuffle to ensure random assignment
                
                # Assign slots
                for entry in available_slots:
                    if hours_remaining <= 0:
                        break  # Stop if all hours are assigned
                    
                    # Ensure the slot is available and not already occupied
                    if not TimetableEntry1.objects.filter(day=entry['day'], period=entry['period'], cls=cls, subject=subject).exists():
                        # Check if the faculty is available for this slot
                        if not TimetableEntry1.objects.filter(day=entry['day'], period=entry['period'], faculty=subject.faculty).exists():
                            # Create a new timetable entry
                            TimetableEntry1.objects.create(
                                day=entry['day'],
                                period=entry['period'],
                                cls=entry['cls'],
                                subject=subject,
                                faculty=subject.faculty
                            )
                            hours_remaining -= 1  # Decrease remaining contact hours
                            empty_slots.remove(entry)  # Remove the slot from available slots

                    # Exit loop when all hours for this subject are assigned
                    if hours_remaining == 0:
                        break
    # return HttpResponse("Timetable generated successfully!")
    return redirect('viewtimetable')

class TimetableView1(View):
    template_name = 'admin/viewtimetable.html'  # Specify your template name here

    def get(self, request, *args, **kwargs):
        # Get all classes
        classes = Class1.objects.all()
        faculties= Faculty1.objects.all()
        
        # Define the days and periods
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        periods = [1, 2, 3, 4, 5]  # Assuming 5 periods per day

        # Initialize a dictionary to hold timetable data
        timetable_data = {cls: {day: {period: None for period in periods} for day in days} for cls in classes}

        # Populate the timetable dictionary with entries
        entries = TimetableEntry1.objects.all()
        for entry in entries:
            timetable_data[entry.cls][entry.day][entry.period] = entry

        # Create a context dictionary for the template
        context = {
            'timetable_data': timetable_data,
            'days': days,
            'periods': periods,
            'faculties':faculties
        }
        
        return render(request, self.template_name, context)

    from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Lab, WorkingDay, TimeSlot

# Lab Views
class AddLab(View):
    def get(self, request):
        labs = Lab.objects.all()
        return render(request, 'admin/addlabs.html', {'labs': labs})

    def post(self, request):
        # Create a new lab
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        Lab.objects.create(name=name, capacity=capacity)
        return redirect('viewlabs')

class Editlab(View):
    def get(self, request, pk):
        lab = Lab.objects.get(pk=pk)
        return render(request, 'admin/editlabs.html', {'lab': lab})

    def post(self, request, pk):
        # Update lab details
        lab = Lab.objects.get(pk=pk)
        lab.name = request.POST.get('name')
        lab.capacity = request.POST.get('capacity')
        lab.save()
        return redirect('viewlabs')

class LabDeleteView(View):
    def get(self, request, pk):
        lab = Lab.objects.get(pk=pk)
        lab.delete()
        return redirect('viewlabs')

class ViewAddedlabs(View):
    def get(self,request):
        lab=Lab.objects.all()
        return render(request,'admin/labs.html',{'labs':lab})

class ViewLabs(View):
    def get(self,request):
        l=Lab.objects.all()
        return render(request,'admin/viewlabs.html',{'labs':l})

class Viewworkingday(View):
    def get(self,request,id):
        d=WorkingDay.objects.filter(lab=id).all()
        print(d)
        e=Lab.objects.filter(id=id).first()
        return render(request,'admin/viewworkingday.html',{'d':d,'e':e})

class Addworkingday(View):
    def get(self,request,id):
        a=Lab.objects.filter(id=id).first()
        return render(request,'admin/addworkingday.html',{'lab':a})

    def post(self,request,id):
        a=Lab.objects.filter(id=id).first()
        c=Addworkingdayform(request.POST)
        if c.is_valid():
            e=c.save(commit=False)
            e.lab=a
            e.save()
            return redirect(reverse('viewworkingday', kwargs={'id': id}))


class Editworkingday(View):
    def get(self,request,id):
        a=WorkingDay.objects.filter(id=id).first()
        return render(request,'admin/updateworkingday.html',{'a':a})


    def post(self,request,id):
        a=WorkingDay.objects.filter(id=id).first()
        c=Addworkingdayform(request.POST,instance=a)
        print(a.lab.id)
        if c.is_valid():
            c.save()
            return redirect(reverse('viewworkingday', kwargs={'id': a.lab.id}))

class Deleteworkingday(View):
    def get(self,request,id):
        a=WorkingDay.objects.filter(id=id).first()
        a.delete()
        return redirect(reverse('viewworkingday', kwargs={'id': a.lab.id}))
    


class Viewtimeslot(View):
    def get(self,request,id):
        t=TimeSlot.objects.filter(working_day__id=id)
        e=WorkingDay.objects.filter(id=id).first()
        # print(e.lab.name)
        # print(e.lab.capacity)
        print(t)
        return render(request,'admin/viewtimeslot.html',{'t':t,'e':e})


class Addtimeslot(View):
    def get(self,request,id):
        a=WorkingDay.objects.filter(id=id).first()
        return render(request,'admin/addslot.html',{'day':a})

    def post(self,request,id):
        a=WorkingDay.objects.filter(id=id).first()
        c=Addslotform(request.POST)
        if c.is_valid():
            e=c.save(commit=False)
            e.working_day=a
            e.save()
            return redirect(reverse('viewtimeslot', kwargs={'id': id}))



class Edittimeslot(View):
    def get(self,request,id):
        a=TimeSlot.objects.filter(id=id).first()
        return render(request,'admin/updateslot.html',{'a':a})


    def post(self,request,id):
        a=TimeSlot.objects.filter(id=id).first()
        c=Addslotform(request.POST,instance=a)
        print(a.working_day.lab.id)
        if c.is_valid():
            print("ggg")
            c.save()
            return redirect(reverse('viewtimeslot', kwargs={'id': a.working_day.id}))

class Deletetimeslot(View):
    def get(self,request,id):
        a=TimeSlot.objects.filter(id=id).first()
        a.delete()
        return redirect(reverse('viewtimeslot', kwargs={'id': a.working_day.id}))




class Staffdashboard(View):
 def get(self,request):
  return render(request,'staff/staffdashboard.html')


class StaffViewnotifications(View):
  def get(self,request):
    o=Staffnotification.objects.all()
    return render(request,'staff/staffviewnotification.html',{'notificationobject':o})


class notificationbystaff(View):
    def get(self,request):

        return render(request,'staff/notificationstaff.html')
    def post(self,request):
        form=Addnotificationbystaffform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staffviewnotification')

class Updatenotificationbystaff(View):
    def get(self,request,id):
        n=Staffnotification.objects.get(id=id)
        return render(request,'staff/updatenotifications.html',{'n':n})
    def post(self,request,id):
        n=Staffnotification.objects.get(id=id)
        form=Updatenotificationform(request.POST,instance=n)
        if form.is_valid():
            form.save()
            return redirect('staffviewnotification')


class Deletenotificationbystaff(View):
    def get(self,request,id):
        n=Staffnotification.objects.get(id=id)
        n.delete()
        return redirect('staffviewnotification')


class TimetableView2(View):
    template_name = 'staff/viewtimetablebystaff.html'  # Specify your template name here

    def get(self, request, *args, **kwargs):
        # Get all classes
        classes = Class1.objects.all()
        faculties= Faculty1.objects.all()
        
        # Define the days and periods
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        periods = [1, 2, 3, 4, 5]  # Assuming 5 periods per day

        # Initialize a dictionary to hold timetable data
        timetable_data = {cls: {day: {period: None for period in periods} for day in days} for cls in classes}

        # Populate the timetable dictionary with entries
        entries = TimetableEntry1.objects.all()
        for entry in entries:
            timetable_data[entry.cls][entry.day][entry.period] = entry

        # Create a context dictionary for the template
        context = {
            'timetable_data': timetable_data,
            'days': days,
            'periods': periods,
            'faculties':faculties
        }
        
        return render(request, self.template_name, context)


class Viewnotificationsaddedbystaff(View):
  def get(self,request):
    notificationobject=Staffnotification.objects.all()
    return render(request,'faculty/viewnotificationsbystaff.html',{'notificationobject':notificationobject})

class TimetableView3(View):
    template_name = 'faculty/viewtimetablebyfaculty.html'  # Specify your template name here

    def get(self, request, *args, **kwargs):
        # Get all classes
        classes = Class1.objects.all()
        faculties= Faculty1.objects.all()
        
        # Define the days and periods
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        periods = [1, 2, 3, 4, 5]  # Assuming 5 periods per day

        # Initialize a dictionary to hold timetable data
        timetable_data = {cls: {day: {period: None for period in periods} for day in days} for cls in classes}

        # Populate the timetable dictionary with entries
        entries = TimetableEntry1.objects.all()
        for entry in entries:
            timetable_data[entry.cls][entry.day][entry.period] = entry

        # Create a context dictionary for the template
        context = {
            'timetable_data': timetable_data,
            'days': days,
            'periods': periods,
            'faculties':faculties
        }
        
        return render(request, self.template_name, context)

class Editprofilebyfaculty(View):
    def get(self,request,id):
        n=Faculty1.objects.get(loginid__id=id)
        return render(request,'faculty/editprofile.html',{'n':n})
    def post(self,request,id):
        n=Faculty1.objects.get(loginid__id=id)
        form=Updatefacultyform(request.POST,instance=n)
        if form.is_valid():
            form.save()
            return redirect('faculty')

class ViewStudent(View):
  def get(self,request):
    st=Student.objects.all()
    print(st)
    return render(request,'admin/viewstudent.html',{'st':st})

class Studentreg(View):
  def get(self,request):
    sem=Class1.objects.all()
    print(sem)
    return render(request,'admin/Student.html',{'sem':sem})
  def post(self,request):
        print('addstudent')
        form=AddStudentform(request.POST)
        if form.is_valid():
            reg_form=form.save(commit=False)
            rf=Userprofile.objects.create_user(user_type='STUDENT',username=request.POST['username'],password=request.POST['password'])
            reg_form.loginid=rf
            rf.save()
            reg_form.save()
        return HttpResponse('''<script>alert("added");window.location="/administrator/viewstudent/"</script>''')
            

class Updatestudent(View):
    def get(self,request,id):
        n=Student.objects.get(id=id)
        s=Class1.objects.all()
        return render(request,'admin/updatestudent.html',{'s':n,'r':s})
    def post(self,request,id):
        print("sss")
        n=Student.objects.get(id=id)
        form=UpdateStudentform(request.POST,instance=n)
        if form.is_valid():
            form.save()
            return redirect('viewstudent')

class Deletestudent(View):
    def get(self,request,id):
        n=Student.objects.get(id=id)
        n.delete()
        return redirect('viewstudent')



# class View(View):
#   def get(self,request):
#     st=Student.objects.all()
#     print(st)
#     return render(request,'admin/viewstudent.html',{'st':st})

# class Studentreg(View):
#   def get(self,request):
#     sem=Class1.objects.all()
#     print(sem)
#     return render(request,'admin/Student.html',{'sem':sem})
#   def post(self,request):
#         print('addstudent')
#         form=AddStudentform(request.POST)
#         if form.is_valid():
#             reg_form=form.save(commit=False)
#             rf=Userprofile.objects.create_user(user_type='STUDENT',username=request.POST['username'],password=request.POST['password'])
#             reg_form.loginid=rf
#             rf.save()
#             reg_form.save()
#         return HttpResponse('''<script>alert("added");window.location="/administrator/viewstudent/"</script>''')
            

# class Updatestudent(View):
#     def get(self,request,id):
#         n=Student.objects.get(id=id)
#         s=Class1.objects.all()
#         return render(request,'admin/updatestudent.html',{'s':n,'r':s})
#     def post(self,request,id):
#         print("sss")
#         n=Student.objects.get(id=id)
#         form=UpdateStudentform(request.POST,instance=n)
#         if form.is_valid():
#             form.save()
#             return redirect('viewstudent')

# class Deletestudent(View):
#     def get(self,request,id):
#         n=Student.objects.get(id=id)
#         n.delete()
#         return redirect('viewstudent')


from django.shortcuts import render, get_object_or_404
from django.views import View
from django.utils import timezone
from calendar import monthrange
from datetime import timedelta, date

from .models import Lab, TimeSlot, Booking, WorkingDay


from django.utils import timezone
from django.views import View
from django.shortcuts import get_object_or_404, render,redirect
from datetime import date, timedelta,datetime
from calendar import monthrange
from .models import Lab, Booking, TimeSlot

class LabBookingView(View):
    def get(self, request, lab_id):
            lab = get_object_or_404(Lab, id=lab_id)

            # Get the current date or use a provided date
            today = timezone.now().date()
            selected_year = int(request.GET.get('year', today.year))
            selected_month = int(request.GET.get('month', today.month))

            selected_date = date(selected_year, selected_month, 1)
            num_days_in_month = monthrange(selected_date.year, selected_date.month)[1]

            first_day_weekday = selected_date.weekday()  # Monday is 0, Sunday is 6

            # Fetch bookings for the selected month
            first_day = selected_date
            last_day = selected_date + timedelta(days=num_days_in_month - 1)
            bookings = Booking.objects.filter(lab=lab, date__range=[first_day, last_day])

            # Create a dictionary of bookings per day
            bookings_by_date = {day: [] for day in range(1, num_days_in_month + 1)}
            for booking in bookings:
                day = booking.date.day
                bookings_by_date[day].append(booking.time_slot)

            calendar_days = []
            for day in range(1, num_days_in_month + 1):
                current_date = date(selected_date.year, selected_date.month, day)
                day_name = current_date.strftime('%A')  # Get day name like 'Monday', 'Tuesday'
                
                # Fetch the working day for this specific day of the week
                working_day = WorkingDay.objects.filter(lab=lab, day=day_name).first()
                # print("working_day",working_day)
                slots_with_status = []

                if working_day:
                    # Fetch only time slots that belong to this working day
                    time_slots = TimeSlot.objects.filter(working_day=working_day)
                    day_bookings = bookings_by_date.get(day, [])
                    print("time_slots",time_slots)
                    for slot in time_slots:
                        is_booked = any(booking == slot for booking in day_bookings)
                        slots_with_status.append({
                            'slot': slot,
                            'status': 'occupied' if is_booked else 'vacant'
                        })

                calendar_days.append({
                    'date': current_date,
                    'slots_with_status': slots_with_status
                })

            # Add the range of empty days before the first day of the month
            empty_days_before_first = list(range(first_day_weekday))

            context = {
                'lab': lab,
                'calendar_days': calendar_days,
                'selected_date': selected_date,
                'selected_year': selected_year,
                'selected_month': selected_month,
                'first_day_weekday': first_day_weekday,
                'empty_days_before_first': empty_days_before_first,
            }
            # print(calendar_days)

            return render(request, 'lab_booking.html', context)
    def post(self, request, lab_id):
        # Handle booking when the user selects a time slot
        lab = get_object_or_404(Lab, id=lab_id)
        user = request.user
        slot_id = request.POST.get('slot_id')
        selected_date = request.POST.get('selected_date')
        purpose=request.POST.get('purpose')
    

        if slot_id and selected_date:
            time_slot = get_object_or_404(TimeSlot, id=slot_id)
            booking_date = datetime.strptime(selected_date, '%b. %d, %Y').date()
            # booking_date = date.fromisoformat(selected_date)

            # Check if the time slot is already booked
            if not Booking.objects.filter(lab=lab, date=booking_date, time_slot=time_slot).exists():
                Booking.objects.create(
                    lab=lab,
                    user=user,
                    date=booking_date,
                    time_slot=time_slot,
                    purpose=purpose
                )
        return self.get(request, lab_id)

class BookingConfirmationView(View):
    def get(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)
        context = {'booking': booking}
        return render(request, 'booking_confirmation.html', context)

class BookingConfirmationView(View):
    def get(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)
        context = {'booking': booking}
        return render(request, 'booking_confirmation.html', context)
    
from django.views import View
from django.shortcuts import get_object_or_404, redirect, render
from .models import Booking
from .forms import BookingForm

class EditBookingView(View):
    def get(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)
        form = BookingForm(instance=booking)
        return render(request, 'edit_booking.html', {'form': form, 'booking': booking})

    def post(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect('lab_booking', lab_id=booking.lab.id)
        return render(request, 'edit_booking.html', {'form': form, 'booking': booking})
from django.views import View
from django.shortcuts import get_object_or_404, redirect, render
from .models import Booking

class DeleteBookingView(View):
    def get(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)
        return render(request, 'delete_confirmation.html', {'booking': booking})

    def post(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)
        booking.delete()
        return redirect('adminlab_booking', lab_id=booking.lab.id)

class AdminLabBookingView(View):
    def get(self, request, lab_id):
        lab = get_object_or_404(Lab, id=lab_id)

        # Get the current date or use a provided date
        today = timezone.now().date()
        selected_year = int(request.GET.get('year', today.year))
        selected_month = int(request.GET.get('month', today.month))

        selected_date = date(selected_year, selected_month, 1)
        num_days_in_month = monthrange(selected_date.year, selected_date.month)[1]

        first_day_weekday = selected_date.weekday()  # Monday is 0, Sunday is 6

        # Fetch bookings for the selected month
        first_day = selected_date
        last_day = selected_date + timedelta(days=num_days_in_month - 1)
        bookings = Booking.objects.filter(lab=lab, date__range=[first_day, last_day])

        # Create a dictionary of bookings per day
        bookings_by_date = {day: [] for day in range(1, num_days_in_month + 1)}
        for booking in bookings:
            day = booking.date.day
            bookings_by_date[day].append(booking)

        calendar_days = []
        for day in range(1, num_days_in_month + 1):
            current_date = date(selected_date.year, selected_date.month, day)
            day_name = current_date.strftime('%A')  # Get day name like 'Monday', 'Tuesday'

            # Fetch the working day for this specific day of the week
            working_day = WorkingDay.objects.filter(lab=lab, day=day_name).first()
            slots_with_status = []

            if working_day:
                # Fetch only time slots that belong to this working day
                time_slots = TimeSlot.objects.filter(working_day=working_day)
                day_bookings = bookings_by_date.get(day, [])
                for slot in time_slots:
                    # Check if the slot is booked
                    booked_slot = next((b for b in day_bookings if b.time_slot == slot), None)
                    slots_with_status.append({
                        'slot': slot,
                        'status': 'occupied' if booked_slot else 'vacant',
                        'booking': booked_slot,  # Pass the booking object if it's occupied
                    })

            calendar_days.append({
                'date': current_date,
                'slots_with_status': slots_with_status
            })

        empty_days_before_first = list(range(first_day_weekday))

        context = {
            'lab': lab,
            'calendar_days': calendar_days,
            'selected_date': selected_date,
            'selected_year': selected_year,
            'selected_month': selected_month,
            'first_day_weekday': first_day_weekday,
            'empty_days_before_first': empty_days_before_first,
        }

        return render(request, 'edit_lab_booking.html', context)

class FacultyViewAddedlabs(View):
    def get(self,request):
        lab=Lab.objects.all()
        return render(request,'faculty/labs.html',{'labs':lab})


class FacultyLabBookingView(View):
    def get(self, request, lab_id):
            lab = get_object_or_404(Lab, id=lab_id)
            user=request.session.get('user_id')
            print(user)

            # Get the current date or use a provided date
            today = timezone.now().date()
            selected_year = int(request.GET.get('year', today.year))
            selected_month = int(request.GET.get('month', today.month))

            selected_date = date(selected_year, selected_month, 1)
            num_days_in_month = monthrange(selected_date.year, selected_date.month)[1]

            first_day_weekday = selected_date.weekday()  # Monday is 0, Sunday is 6

            # Fetch bookings for the selected month
            first_day = selected_date
            last_day = selected_date + timedelta(days=num_days_in_month - 1)
            bookings = Booking.objects.filter(lab=lab, date__range=[first_day, last_day])

            # Create a dictionary of bookings per day
            bookings_by_date = {day: [] for day in range(1, num_days_in_month + 1)}
            for booking in bookings:
                day = booking.date.day
                bookings_by_date[day].append(booking.time_slot)

            calendar_days = []
            for day in range(1, num_days_in_month + 1):
                current_date = date(selected_date.year, selected_date.month, day)
                day_name = current_date.strftime('%A')  # Get day name like 'Monday', 'Tuesday'
                
                # Fetch the working day for this specific day of the week
                working_day = WorkingDay.objects.filter(lab=lab, day=day_name).first()
                # print("working_day",working_day)
                slots_with_status = []

                if working_day:
                    # Fetch only time slots that belong to this working day
                    time_slots = TimeSlot.objects.filter(working_day=working_day)
                    day_bookings = bookings_by_date.get(day, [])
                    print("time_slots",time_slots)
                    for slot in time_slots:
                        is_booked = any(booking == slot for booking in day_bookings)
                        slots_with_status.append({
                            'slot': slot,
                            'status': 'occupied' if is_booked else 'vacant'
                        })

                calendar_days.append({
                    'date': current_date,
                    'slots_with_status': slots_with_status
                })

            # Add the range of empty days before the first day of the month
            empty_days_before_first = list(range(first_day_weekday))

            context = {
                'lab': lab,
                'calendar_days': calendar_days,
                'selected_date': selected_date,
                'selected_year': selected_year,
                'selected_month': selected_month,
                'first_day_weekday': first_day_weekday,
                'empty_days_before_first': empty_days_before_first,
            }
            # print(calendar_days)

            return render(request, 'faculty/lab_booking.html', context)
    def post(self, request, lab_id):
        # Handle booking when the user selects a time slot
        lab = get_object_or_404(Lab, id=lab_id)
        user = Userprofile.objects.get(id=request.session.get('user_id'))
        print(user)
        slot_id = request.POST.get('slot_id')
        selected_date = request.POST.get('selected_date')
        purpose=request.POST.get('purpose')
    

        if slot_id and selected_date:
            time_slot = get_object_or_404(TimeSlot, id=slot_id)
            booking_date = datetime.strptime(selected_date, '%b. %d, %Y').date()
            # booking_date = date.fromisoformat(selected_date)

            # Check if the time slot is already booked
            if not Booking.objects.filter(lab=lab, date=booking_date, time_slot=time_slot).exists():
                Booking.objects.create(
                    lab=lab,
                    user=user,
                    date=booking_date,
                    time_slot=time_slot,
                    purpose=purpose
                )
        return self.get(request, lab_id)






