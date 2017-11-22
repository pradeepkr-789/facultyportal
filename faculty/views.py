from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.views import login as auth_login
from django.contrib.auth import password_validation
from django.http import Http404,HttpResponse,HttpResponseRedirect,JsonResponse
import re
# Create your views here.
from .models import faculty_profile,student,department,thesis,project,recognitions


def home(request):
    if request.user and not request.user.is_anonymous:
        return HttpResponse("logged in")
    else:
        return HttpResponse("not logged in")

def signup(request):
    if request.user and not request.user.is_anonymous:
        return redirect(home)
    else:
        if request.method == "GET":
            errors = {'firstname': False,
                      'lastname': False,
                      'email': False,
                      'pass': False,
                      'verpass': False,
                      'department': False,
                      'designation': False,
                      'officephone': False,
                      'officeadd':False,
                      'homephone': False,
                      'homeadd': False}
            context = {
                'designations': faculty_profile.designation_values,
                'departments': department.objects.all().values_list('name','full_name'),
                'errors':errors

            }
            return render(request, 'signup.html', context)
        if request.method == "POST":
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            email = request.POST.get('email')
            passwd = request.POST.get('pass')
            verpasswd = request.POST.get('verpass')
            dept = request.POST.get('department')
            designation = request.POST.get('designation')
            officephone = request.POST.get('officephone')
            homephone = request.POST.get('homephone')
            officeadd = request.POST.get('officeadd')
            homeadd = request.POST.get('homeadd')
            # print(firstname, lastname, email, passwd, verpasswd, dept, designation, officephone, homephone, officeadd, homeadd, sep="\n")
            errors = {'firstname':False,
                      'lastname':False,
                      'email':False,
                      'pass':False,
                      'verpass':False,
                      'department':False,
                      'designation':False,
                      'officephone':False,
                      'officeadd':False,
                      'homephone':False,
                      'homeadd':False}
            if not re.match(r'(^[a-zA-Z0-9_.+-]+@iitg\.ernet\.in$)',email):
                errors['email']=True
            elif User.objects.filter(email=email):
                errors['email']=True
            if not firstname:
                errors['firstname']=True
            if not lastname:
                errors['lastname']=True
            if passwd != verpasswd:
                errors['verpass']=True
            else:
                try:
                    password_validation.validate_password(passwd)
                except password_validation.ValidationError:
                    errors['pass']=True
            if department.objects.filter(name=dept).count()==0:
                errors['department']=True
            if designation not in dict(faculty_profile.designation_values).keys():
                errors['designation']=True
            if not officephone.isnumeric() or not len(officephone)==4:
                errors['officephone']=True
            if not homephone.isnumeric() or not len(homephone)==4:
                errors['homephone']=True
            # print(errors)
            for error in errors.values():
                if error:
                    context={
                        'designations': faculty_profile.designation_values,
                        'departments': department.objects.all().values_list('name','full_name'),
                        'errors': errors
                    }
                    return render(request,'signup.html',context)
            user = User.objects.create_user(first_name=firstname,last_name=lastname, username=email[:-14],email=email, password=passwd)
            user.save()
            if 'room' not in officeadd.lower():
                officeadd = 'Room No. '+officeadd
            fac_profile = faculty_profile(userid=user, office_address=officeadd, office_phone='+91-361-258'+officephone, home_address=homeadd, home_phone='+91-361-258'+homephone, designation=designation)
            fac_profile.save()
            department.objects.filter(name=dept).first().professors.add(user)
            return redirect('/auth/login')

def stud_profile(request,rollno):
    if request.method == 'GET':
        stud = student.objects.filter(rollno=rollno)
        if stud.count()==1:
            stud = stud.first()
        else:
            return Http404
        thes = thesis.objects.filter(student=stud.id)
        context = {
            'student':stud,
            'thesis':thes
        }
        return render(request,'student_profile.html',context)
    else:
        return Http404