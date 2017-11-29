from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.views import login as auth_login
from django.contrib.auth import password_validation
from django.http import Http404,HttpResponse,HttpResponseRedirect,JsonResponse
import re
# Create your views here.
from .models import faculty_profile,student,department,publication,project,recognition,teaching,workexperience


def home(request):
    if request.method == 'GET':
        if request.user and not request.user.is_anonymous:
            logged_in = True
        else:
            logged_in = False
        if logged_in:
            context = {
                'logged_in': logged_in,
                'name':request.user.get_full_name,
                'username':request.user.username
            }
            return render(request,'home.html', context)
        else:
            context = {
                'logged_in': logged_in,
            }
            return render(request, 'home.html', context)

def logout(request):
    auth_logout(request)
    return redirect(home)

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
                print('a')
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
                        'errors': errors,
                        'logged_in': False,
                    }
                    return render(request,'signup.html',context)
            user = User.objects.create_user(first_name=firstname,last_name=lastname, username=email[:-14],email=email, password=passwd)
            user.save()
            if 'room' not in officeadd.lower():
                officeadd = 'Room No. '+officeadd
            fac_profile = faculty_profile(user=user, office_address=officeadd, office_phone='+91-361-258'+officephone, home_address=homeadd, home_phone='+91-361-258'+homephone, designation=designation)
            fac_profile.save()
            department.objects.filter(name=dept).first().professors.add(user)
            return HttpResponseRedirect('/auth/login')

def profile(request, username):
    if request.method == 'GET':
        user = User.objects.filter(username=username).first()
        if not user:
            raise Http404
        fac_profile = faculty_profile.objects.filter(user = user.id).first()
        if user.username == request.user.username:
            editable = True
        else:
            editable = False
        if request.user and not request.user.is_anonymous:
            logged_in = True
        else:
            logged_in = False
        context = {
            'editable': editable,
            'logged_in':logged_in,
            'profile':fac_profile,
            'email':user.email,
            'name':user.get_full_name,
            'username': user.username
        }
        return render(request,'profile.html',context)
    elif request.method == 'POST':
        raise Http404

def profileedit(request, username):
    if request.user and not request.user.is_anonymous:
        if request.user.username == username:
            if request.method == 'GET':
                user = User.objects.filter(username=username).first()
                if not user:
                    raise Http404
                fac_profile = faculty_profile.objects.filter(user=user.id).first()
                designations = faculty_profile.designation_values
                context = {
                    'faculty_profile': fac_profile,
                    'email': user.email,
                    'firstname': user.first_name,
                    'lastname': user.last_name,
                    'username': username,
                    'designations':designations,
                    'name': user.get_full_name,
                    'logged_in': True,
                }
                return render(request,'profileedit.html',context)
            elif request.method == 'POST':
                user = User.objects.filter(username=username).first()
                if not User:
                    raise Http404
                fac_profile = faculty_profile.objects.filter(user=user.id).first()
                designations = faculty_profile.designation_values
                firstname = request.POST.get('firstname')
                lastname = request.POST.get('lastname')
                designation = request.POST.get('designation')
                officephone = request.POST.get('officephone')
                homephone = request.POST.get('homephone')
                officeadd = request.POST.get('officeadd')
                homeadd = request.POST.get('homeadd')
                researchinterest = request.POST.get('researchinterest')
                primaryresearchgroup = request.POST.get('primaryresearchgroup')
                aboutphd = request.POST.get('aboutphd')
                aboutmasters = request.POST.get('aboutmasters')
                aboutbatchelor = request.POST.get('aboutbatchelor')
                fac_profile.designation = designation
                user.first_name = firstname
                user.last_name = lastname
                fac_profile.office_phone = officephone
                fac_profile.home_phone = homephone
                fac_profile.office_address = officeadd
                fac_profile.home_address = homeadd
                fac_profile.research_interest = researchinterest
                fac_profile.primary_research_group = primaryresearchgroup
                fac_profile.education_phd = aboutphd
                fac_profile.education_masters = aboutmasters
                fac_profile.education_batchelor = aboutbatchelor
                fac_profile.save()
                user.save()
                context = {
                    'faculty_profile': fac_profile,
                    'email': user.email,
                    'firstname': user.first_name,
                    'lastname': user.last_name,
                    'username': username,
                    'designations': designations,
                    'name': user.get_full_name,
                    'logged_in': True
                }
                return render(request,'profileedit.html',context)
        else:
            raise Http404
    else:
        return HttpResponseRedirect('/auth/login')

def projectsview(request,username):
    if request.method == 'GET':
        user = User.objects.filter(username=username).first()
        if not user:
            raise Http404
        if user.username == request.user.username:
            editable = True
        else:
            editable = False
        if request.user and not request.user.is_anonymous:
            logged_in = True
        else:
            logged_in = False
        projects = project.objects.filter(user=user.id)

        context = {
            'editable':editable,
            'logged_in': logged_in,
            'projects': projects,
            'name':user.get_full_name,
            'username':username
        }
        return render(request,'projects.html', context)
    elif request.method == 'POST':
        raise Http404

def projectadd(request,username):
    if request.method == 'GET':
        user = User.objects.filter(username=username).first()
        if not user:
            raise Http404
        if user.username == request.user.username:
            editable = True
        else:
            editable = False
        if request.user and not request.user.is_anonymous:
            logged_in = True
        else:
            logged_in = False
        context = {
            'editable':editable,
            'logged_in': logged_in,
            'name':user.get_full_name,
            'username':user.username
        }
        return render(request,'projectadd.html', context)
    elif request.method == 'POST':
        user = User.objects.filter(username=username).first()
        if not user:
            raise Http404
        if user.username == request.user.username:
            editable = True
        else:
            editable = False
        if request.user and not request.user.is_anonymous:
            logged_in = True
        else:
            logged_in = False
        projecttitle = request.POST.get('projecttitle')
        principal_investigator = request.POST.get('pi')
        co_investigator = request.POST.get('copi')
        fundingagency = request.POST.get('fundingagency')
        start_year = request.POST.get('startyear')
        end_year = request.POST.get('endyear')
        new_project = project(user=user, title=projecttitle, principal_investigator=principal_investigator, co_investigator=co_investigator, funding_agency=fundingagency, start_year=start_year, end_year=end_year)
        new_project.save()
        projects = project.objects.filter(user=user.id)
        context = {
            'editable': editable,
            'logged_in': logged_in,
            'projects': projects,
            'name': user.get_full_name,
            'username': user.username
        }
        return render(request,'projects.html', context)

def projectdel(request,username):
    if request.method == 'GET':
        raise Http404
    elif request.method == 'POST':
        user = User.objects.filter(username=username).first()
        if not user:
            raise Http404
        if user.username == request.user.username:
            editable = True
        else:
            editable = False
        if request.user and not request.user.is_anonymous:
            logged_in = True
        else:
            logged_in = False
        projectid = request.POST.get('projectid')
        del_project = project.objects.all().filter(id=projectid).first()
        if del_project:
            if del_project.user.id == request.user.id:
                del_project.delete()
                projects = project.objects.filter(user=user.id)
                context = {
                    'editable': editable,
                    'logged_in': logged_in,
                    'projects': projects,
                    'name': user.get_full_name,
                    'username': user.username
                }
                return render(request, 'projects.html', context)
            else:
                projects = project.objects.filter(user=user.id)
                context = {
                    'editable': editable,
                    'logged_in': logged_in,
                    'projects': projects,
                    'name': user.get_full_name,
                    'username': user.username
                }
                return render(request, 'projects.html', context)
        else:
            projects = project.objects.filter(user=user.id)
            context = {
                'editable': editable,
                'logged_in': logged_in,
                'projects': projects,
                'name': user.get_full_name,
                'username': user.username
            }
            return render(request, 'projects.html', context)

def publicationsview(request,username):
    if request.method == 'GET':
        user = User.objects.filter(username=username).first()
        if not user:
            raise Http404
        if user.username == request.user.username:
            editable = True
        else:
            editable = False
        if request.user and not request.user.is_anonymous:
            logged_in = True
        else:
            logged_in = False
        publications = publication.objects.filter(user=user.id)

        context = {
            'editable':editable,
            'logged_in': logged_in,
            'publications': publications,
            'name':user.get_full_name,
            'username':username
        }
        return render(request,'publications.html', context)
    elif request.method == 'POST':
        raise Http404

def publicationadd(request,username):
    if request.method == 'GET':
        user = User.objects.filter(username=username).first()
        if not user:
            raise Http404
        if user.username == request.user.username:
            editable = True
        else:
            editable = False
        if request.user and not request.user.is_anonymous:
            logged_in = True
        else:
            logged_in = False
        context = {
            'editable':editable,
            'logged_in': logged_in,
            'name':user.get_full_name,
            'username':user.username
        }
        return render(request,'publicationadd.html', context)
    elif request.method == 'POST':
        user = User.objects.filter(username=username).first()
        if not user:
            raise Http404
        if user.username == request.user.username:
            editable = True
        else:
            editable = False
        if request.user and not request.user.is_anonymous:
            logged_in = True
        else:
            logged_in = False
        publicationtitle = request.POST.get('publicationtitle')
        desc = request.POST.get('desc')
        contrib = request.POST.get('contrib')
        publishedin = request.POST.get('publishedin')
        publishedtime = request.POST.get('publishtime')

        new_publication = publication(user=user,title=publicationtitle, description=desc, contributors=contrib, published_in=publishedin, time_published=publishedtime)
        new_publication.save()

        publications = publication.objects.filter(user=user.id)
        context = {
            'editable': editable,
            'logged_in': logged_in,
            'publications': publications,
            'name': user.get_full_name,
            'username':user.username
        }
        return render(request,'projects.html', context)

def publicationdel(request, username):
    if request.method == 'GET':
        raise Http404
    elif request.method == 'POST':
        user = User.objects.filter(username=username).first()
        if not user:
            raise Http404
        if user.username == request.user.username:
            editable = True
        else:
            editable = False
        if request.user and not request.user.is_anonymous:
            logged_in = True
        else:
            logged_in = False
        publicationid = request.POST.get('publicationid')
        del_publication = publication.objects.all().filter(id=publicationid).first()
        if del_publication:
            if del_publication.user.id == request.user.id:
                del_publication.delete()
                publications = publication.objects.filter(user=user.id)
                context = {
                    'editable': editable,
                    'logged_in': logged_in,
                    'publications': publications,
                    'name': user.get_full_name,
                    'username': user.username
                }
                return render(request, 'publications.html', context)
            else:
                publications = publication.objects.filter(user=user.id)
                context = {
                    'editable': editable,
                    'logged_in': logged_in,
                    'publications': publications,
                    'name': user.get_full_name,
                    'username': user.username
                }
                return render(request, 'publications.html', context)
        else:
            publications = publication.objects.filter(user=user.id)
            context = {
                'editable': editable,
                'logged_in': logged_in,
                'publications': publications,
                'name': user.get_full_name,
                'username': user.username
            }
            return render(request, 'publications.html', context)

def recognitionsview(request,username):
    if request.method == 'GET':
        user = User.objects.filter(username=username).first()
        if not user:
            raise Http404
        if user.username == request.user.username:
            editable = True
        else:
            editable = False
        if request.user and not request.user.is_anonymous:
            logged_in = True
        else:
            logged_in = False
        recognitions = recognition.objects.filter(user=user.id)

        context = {
            'editable':editable,
            'logged_in': logged_in,
            'recognitions': recognitions,
            'name':user.get_full_name,
            'username':username
        }
        return render(request,'recognitions.html', context)
    elif request.method == 'POST':
        raise Http404

def recognitionadd(request,username):
    if request.method == 'GET':
        user = User.objects.filter(username=username).first()
        if not user:
            raise Http404
        if user.username == request.user.username:
            editable = True
        else:
            editable = False
        if request.user and not request.user.is_anonymous:
            logged_in = True
        else:
            logged_in = False
        context = {
            'editable':editable,
            'logged_in': logged_in,
            'name':user.get_full_name,
            'username':user.username
        }
        return render(request,'recognitionadd.html', context)
    elif request.method == 'POST':
        user = User.objects.filter(username=username).first()
        if not user:
            raise Http404
        if user.username == request.user.username:
            editable = True
        else:
            editable = False
        if request.user and not request.user.is_anonymous:
            logged_in = True
        else:
            logged_in = False
        recognitiontitle = request.POST.get('recognitiontitle')
        desc = request.POST.get('desc')
        givenby = request.POST.get('givenby')
        new_recognition = recognition(user=user,title=recognitiontitle, description=desc, given_by=givenby)
        new_recognition.save()

        recognitions = recognition.objects.filter(user=user.id)
        context = {
            'editable': editable,
            'logged_in': logged_in,
            'recognitions': recognitions,
            'name': user.get_full_name,
            'username':user.username
        }
        return render(request,'recognitions.html', context)

def recognitiondel(request, username):
    if request.method == 'GET':
        raise Http404
    elif request.method == 'POST':
        user = User.objects.filter(username=username).first()
        if not user:
            raise Http404
        if user.username == request.user.username:
            editable = True
        else:
            editable = False
        if request.user and not request.user.is_anonymous:
            logged_in = True
        else:
            logged_in = False
        recognitionid = request.POST.get('recognitionid')
        del_recognition = recognition.objects.all().filter(id=recognitionid).first()
        if del_recognition:
            if del_recognition.user.id == request.user.id:
                del_recognition.delete()
                recognitions = recognition.objects.filter(user=user.id)
                context = {
                    'editable': editable,
                    'logged_in': logged_in,
                    'recognitions': recognitions,
                    'name': user.get_full_name,
                    'username': user.username
                }
                return render(request, 'recognitions.html', context)
            else:
                recognitions = recognition.objects.filter(user=user.id)
                context = {
                    'editable': editable,
                    'logged_in': logged_in,
                    'recognitions': recognitions,
                    'name': user.get_full_name,
                    'username': user.username
                }
                return render(request, 'recognitions.html', context)
        else:
            recognitions = recognition.objects.filter(user=user.id)
            context = {
                'editable': editable,
                'logged_in': logged_in,
                'recognitions': recognitions,
                'name': user.get_full_name,
                'username': user.username
            }
            return render(request, 'recognitions.html', context)

def experiencesview(request,username):
    if request.method == 'GET':
        user = User.objects.filter(username=username).first()
        if not user:
            raise Http404
        if user.username == request.user.username:
            editable = True
        else:
            editable = False
        if request.user and not request.user.is_anonymous:
            logged_in = True
        else:
            logged_in = False
        experiences = workexperience.objects.filter(user=user.id)

        context = {
            'editable':editable,
            'logged_in': logged_in,
            'experiences': experiences,
            'name':user.get_full_name,
            'username':username
        }
        return render(request,'experiences.html', context)
    elif request.method == 'POST':
        raise Http404

def experienceadd(request,username):
    if request.method == 'GET':
        user = User.objects.filter(username=username).first()
        if not user:
            raise Http404
        if user.username == request.user.username:
            editable = True
        else:
            editable = False
        if request.user and not request.user.is_anonymous:
            logged_in = True
        else:
            logged_in = False
        context = {
            'editable':editable,
            'logged_in': logged_in,
            'name':user.get_full_name,
            'username':user.username
        }
        return render(request,'experienceadd.html', context)
    elif request.method == 'POST':
        user = User.objects.filter(username=username).first()
        if not user:
            raise Http404
        if user.username == request.user.username:
            editable = True
        else:
            editable = False
        if request.user and not request.user.is_anonymous:
            logged_in = True
        else:
            logged_in = False
        job_title = request.POST.get('job_title')
        organisation = request.POST.get('organisation')
        startyear = request.POST.get('startyear')
        endyear = request.POST.get('endyear')
        new_workexperience = workexperience(user=user,job_title=job_title, organisation=organisation, start_year=startyear, end_year=endyear)
        new_workexperience.save()

        experiences = workexperience.objects.filter(user=user.id)
        context = {
            'editable': editable,
            'logged_in': logged_in,
            'experiences': experiences,
            'name': user.get_full_name,
            'username':user.username
        }
        return render(request,'experiences.html', context)

def experiencedel(request, username):
    if request.method == 'GET':
        raise Http404
    elif request.method == 'POST':
        user = User.objects.filter(username=username).first()
        if not user:
            raise Http404
        if user.username == request.user.username:
            editable = True
        else:
            editable = False
        if request.user and not request.user.is_anonymous:
            logged_in = True
        else:
            logged_in = False
        experienceid = request.POST.get('experienceid')
        del_experience = workexperience.objects.all().filter(id=experienceid).first()
        if del_experience:
            if del_experience.user.id == request.user.id:
                del_experience.delete()
                experiences = workexperience.objects.filter(user=user.id)
                context = {
                    'editable': editable,
                    'logged_in': logged_in,
                    'experiences': experiences,
                    'name': user.get_full_name,
                    'username': user.username
                }
                return render(request, 'experiences.html', context)
            else:
                experiences = workexperience.objects.filter(user=user.id)
                context = {
                    'editable': editable,
                    'logged_in': logged_in,
                    'experiences': experiences,
                    'name': user.get_full_name,
                    'username': user.username
                }
                return render(request, 'experiences.html', context)
        else:
            experiences = workexperience.objects.filter(user=user.id)
            context = {
                'editable': editable,
                'logged_in': logged_in,
                'experiences': experiences,
                'name': user.get_full_name,
                'username': user.username
            }
            return render(request, 'experiences.html', context)

def departmentview(request,name):
    if request.method == 'GET':
        user = request.user
        if request.user and not request.user.is_anonymous:
            logged_in = True
        else:
            logged_in = False
        department_obj = department.objects.filter(name=name).first()

        if department_obj:
            profiles_users=[]
            professors=department_obj.professors.all()
            for i in range(professors.count()):
                profile = faculty_profile.objects.filter(user=professors[i].id).first()
                profiles_users.append((professors[i],profile))
            designation_values = dict(faculty_profile.designation_values)
            context = {
                'logged_in': logged_in,
                'department': department_obj,
                'profiles_users':profiles_users,
                'designations':designation_values,
                'username':user.username
            }
            return render(request,'department.html', context)
        else:
            raise Http404
    elif request.method == 'POST':
        raise Http404
