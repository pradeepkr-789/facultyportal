from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime


# Create your models here.

class faculty_profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
        (prof, 'Professor'),
        (head, 'Professor and Head'),
        (hnr_prof, 'Honarary Professor'),
        (vst_prof, 'Visiting Professor')
    )
    designation = models.CharField(
        max_length=4, choices=designation_values, default=asst_prof, null=False)
    research_interest = models.CharField(max_length=1000, null=True, blank=True)
    primary_research_group = models.CharField(max_length=1000, null=True, blank=True)
    education_phd = models.CharField(max_length=1000, null=True, blank=True)
    education_masters = models.CharField(max_length=1000, null=True, blank=True)
    education_batchelor = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.user.username + " " + self.user.get_full_name()


class student(models.Model):
    btech = 'bt'
    mtech = 'mt'
    phd = 'ph'
    msc = 'ms'
    bdes = 'bd'
    mdes = 'md'
    program_values = (
        (btech, 'BTech'),
        (mtech, 'MTech'),
        (phd, 'PhD'),
        (msc, 'MSc'),
        (bdes, 'BDes'),
        (mdes, 'MDes')
    )
    name = models.CharField(max_length=250, null=False, blank=False)
    rollno = models.IntegerField()
    program = models.CharField(
        max_length=2,
        choices=program_values
    )
    joining_year = models.IntegerField(validators=[MinValueValidator(1994), MaxValueValidator(datetime.datetime.now().year)])
    passing_year = models.IntegerField(validators=[MinValueValidator(1994), MaxValueValidator(datetime.datetime.now().year)])
    thesis_title = models.CharField(max_length=500, null=False)
    thesis_description = models.CharField(max_length=25000, null=True, blank=True)
    thesis_supervisors = models.ManyToManyField(User)

    def __str__(self):
        return str(self.rollno) + " " + self.name


class project(models.Model):
    title = models.CharField(max_length=500, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    principal_investigator = models.CharField(max_length=500, null=False)
    co_investigator = models.CharField(max_length=500, null=True, blank=True)
    funding_agency = models.CharField(max_length=200, null=True, blank=True)
    start_year = models.IntegerField(null=False, validators=[MaxValueValidator(datetime.datetime.now().year)])
    end_year = models.IntegerField(null=True, blank=True, validators=[MaxValueValidator(datetime.datetime.now().year)])
    website = models.URLField(null=True, blank=True)

    def __str__(self):
        return  self.title + ", " + self.principal_investigator


class recognition(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=500, null=False)
    given_by = models.CharField(max_length=200, null=False)
    description = models.CharField(max_length=25000,null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name() + " " + self.title


class publication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=500, null=False)
    description = models.CharField(max_length=25000, null=False, blank=True)
    published_in = models.CharField(max_length=500, null=False)
    time_published = models.CharField(max_length=50, null=True, blank=True)
    contributors = models.CharField(max_length=500, null=False)

    def __str__(self):
        return self.user.get_full_name() + " " + self.title


class teaching(models.Model):
    professors = models.ManyToManyField(User)
    course_name = models.CharField(max_length=500, null=False)
    course_title = models.CharField(max_length=500, null=False)
    academic_year_start = models.IntegerField(validators=[MinValueValidator(1994),MinValueValidator(datetime.datetime.now().year)])
    semesters=(
        ('even', 'Even Semester'),
        ('odd', 'Odd Semester')
    )
    semester = models.CharField(max_length=4, choices=semesters)

    def __str__(self):
        return self.course_title + ": " + self.course_name + ", " + str(self.academic_year_start) + "-" + str(self.academic_year_start+1) +", " + dict(self.semesters)[self.semester]


class department(models.Model):
    name = models.CharField(max_length=10, null=False)
    full_name = models.CharField(max_length=50, null=False)
    professors = models.ManyToManyField(User)
    students = models.ManyToManyField(student)
    department_cover = models.ImageField(upload_to='department_covers', null=True, blank=True)
    department_logo = models.ImageField(upload_to='department_logos', null=True, blank=True)
    def __str__(self):
        return self.full_name

class workexperience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length = 1000, null=False)
    organisation = models.CharField(max_length = 2000, null=False)
    start_year = models.IntegerField(null=False, validators=[MaxValueValidator(datetime.datetime.now().year)])
    end_year = models.IntegerField(null=True, blank=True, validators=[MaxValueValidator(datetime.datetime.now().year)])
    def __str__(self):
        return self.user.get_full_name() + " " + self.job_title + " " + self.organisation