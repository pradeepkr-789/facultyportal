from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
# Create your models here.

class faculty_profile(models.Model):
    userid = models.ForeignKey(User,on_delete=models.CASCADE)
    userimage = models.ImageField(upload_to='faculty_profile_pics', null=True, blank=True)
    office_address = models.CharField(max_length=250, null=True, blank=True)
    office_phone = models.CharField(max_length=30, null=True, blank=True)
    home_address = models.CharField(max_length=250, null=True, blank=True)
    home_phone = models.CharField(max_length=30, null=True, blank=True)
    prof = 'pro'
    head = 'hod'
    asc_prof = 'asc'
    asst_prof = 'ast'
    hnr_prof = 'hon'
    vst_prof = 'vst'
    designation_values = (
        (asst_prof, 'Assistant Professor'),
        (asc_prof, 'Associate Professor'),
        (prof,'Professor'),
        (head,'Professor and Head'),
        (hnr_prof,'Honarary Professor'),
        (vst_prof,'Visiting Professor')
    )
    designation = models.CharField(
        max_length=4, choices=designation_values, default=asst_prof)
    def __str__(self):
        return self.userid.first_name+" "+self.userid.last_name

class student(models.Model):
    btech = 'bt'
    mtech = 'mt'
    phd = 'ph'
    msc = 'ms'
    bdes = 'bd'
    mdes = 'md'
    program_values = (
        (btech,'BTech'),
        (mtech,'MTech'),
        (phd,'PhD'),
        (msc,'MSc'),
        (bdes,'BDes'),
        (mdes,'MDes')
    )
    name = models.CharField(max_length=250, null=False, blank=False)
    rollno = models.IntegerField()
    program = models.CharField(
        max_length=2,
        choices=program_values
    )
    joining_year = models.IntegerField()
    passing_year = models.IntegerField()

    def __str__(self):
        return self.name

class thesis(models.Model):
    title = models.CharField(max_length=500, null=False)
    student = models.ForeignKey(student,on_delete=models.CASCADE)
    supervisors = models.ManyToManyField(User)
    def __str__(self):
        return self.title

class project(models.Model):
    title = models.CharField(max_length=500, null=False)
    principal_investigator = models.ManyToManyField(User,related_name='pi')
    co_investigator = models.ManyToManyField(User,related_name='copi')
    funding_agency = models.CharField(max_length=200, null=True)
    start_year = models.IntegerField()
    end_year = models.IntegerField(null=True,blank=True)
    def __str__(self):
        return self.title

class recognitions(models.Model):
    title = models.CharField(max_length=200)
    given_by = models.CharField(max_length=200)
    def __str__(self):
        return self.title



class department(models.Model):
    name = models.CharField(max_length=10, null=False)
    full_name = models.CharField(max_length=50, null=False)
    professors = models.ManyToManyField(User)
    students = models.ManyToManyField(student)
    def __str__(self):
        return self.full_name