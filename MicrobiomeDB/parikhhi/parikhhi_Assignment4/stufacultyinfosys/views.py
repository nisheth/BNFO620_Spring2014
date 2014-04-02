# Views

import sys
import re

# Import modules
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,Group,Permission
from django.db import IntegrityError

# Import models
from models import Major
from models import Course
from models import Faculty
from models import Student

# Import forms
from forms import LoginForm
from forms import RegisterForm
from forms import AddMajorForm
from forms import AddCourseForm
from forms import RegisterCourseForm

def home(request):
	return render(request, 'stufacultyinfosys/home.html')


def login(request,next='/'):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			#authenticate the user
			user = authenticate(username=username, password=password)
			if user:
				if user.is_active:
					login_user(request,user)
					return redirect(next)
			else:
				message = "Sorry you have entered an invalid username or password"
				params = {
					'form': form,
					'message': message,
					}
				return render(request,'stufacultyinfosys/login.html',params)
    
			return render(request,'stufacultyinfosys/login.html',params)
	else:
		form = LoginForm()
		params = {
			'form':form,
			}
		return render(request,'stufacultyinfosys/login.html',params)


def logout(request):
	logout_user(request)
	return redirect('/')


def register(request):
	
	if request.method == "POST":
		form = RegisterForm(request.POST)
		if form.is_valid():
			firstname = request.POST['firstname']
			lastname = request.POST['lastname']
			majorcode = request.POST['majorcode']
			major = Major.objects.get(pk=majorcode)		# major object
			usertype = request.POST['usertype']
			useremail = request.POST['useremail']
			username = request.POST['username']
			password1 = request.POST['password1']
			password2 = request.POST['password2']

			if password2 == password1:
			
				try:
					#create user 
					user = User.objects.create_user(username, useremail, password1)
					user.first_name = firstname
					user.last_name = lastname
					user.save()
					#Create Student/Faculty objects, groups, add user and assign permissions
					if usertype == "Faculty":
						faculty = Faculty.createFaculty(firstname, lastname, useremail, username, password1, major)
						Faculty_group, created = Group.objects.get_or_create(name='Faculty User')
						if created:
							canAddMajor = Permission.objects.get(name='Can add major')
							canAddCourse = Permission.objects.get(name='Can add course')
							Faculty_group.permissions.add(canAddMajor)
							Faculty_group.permissions.add(canAddCourse)
						user.groups.add(Faculty_group)
					else :
						student = Student.createStudent(firstname, lastname, useremail, username, password1, major)
						Student_group, created = Group.objects.get_or_create(name='Student User')
						user.groups.add(Student_group)

				except IntegrityError as e:
					params = {
						'form' : form,
						'message' : e,
						}
					return render(request,'stufacultyinfosys/register.html',params)


				# User authentication
				if user:
					userlog = authenticate(username=username, password=password1)
					if userlog:
						if user.is_active:
							login_user(request, userlog)
							message = "You have been successfully logged in!"
							params = {
								'form': form,
								'message':message,
								}
							return render(request,'stufacultyinfosys/register.html',params)

				else:
					message = "Error in logging in.\nPlease contact Hardik Parikh at parikhhi@vcu.edu"
					params = {
						'form': form,
						'message':message,
						}
					return render(request,'stufacultyinfosys/register.html',params)

			else:
				message = "Passwords do not match!"
				params = {
					'form' : form,
					'message' : message,
					}
				return render(request,'stufacultyinfosys/register.html',params)

	else:
		form = RegisterForm()
		params = {
			'form':form,
			}
		return render(request,'stufacultyinfosys/register.html',params)


@login_required()
def facultyhome(request):
        return render(request, 'stufacultyinfosys/facultyhome.html')


@login_required()
def addMajor(request):
	if request.method == "POST":
		form = AddMajorForm(request.POST)
		if form.is_valid():
			user = request.user
			canAddMajor = user.has_perm('stufacultyinfosys.add_major')
			facultyusername = request.POST['facultyusername']
			majorcode = request.POST['majorcode']
			majorfullname = request.POST['majorfullname']
			if facultyusername == user.username:
				try:
					major = Major.createMajor(majorcode, majorfullname)
					params = {
						'form':form,
						'canAddMajor':canAddMajor,
						'major':major,
						}			
					return render(request, 'stufacultyinfosys/addmajor.html', params)
				except IntegrityError as e:
					params = {
						'form' : form,
						'message' : e,
						}
					return render(request,'stufacultyinfosys/addmajor.html',params)
			else:
				message = "Incorrect username !"
				params = {
					'form':form,
					'message':message,
					'canAddMajor':canAddMajor,
					}
				return render(request, 'stufacultyinfosys/addmajor.html', params)
	else:
		user = request.user
		canAddMajor = user.has_perm('stufacultyinfosys.add_major')
		form = AddMajorForm()
		params = {
			'form':form,
			'canAddMajor':canAddMajor,
			}
		return render(request, 'stufacultyinfosys/addmajor.html', params)


@login_required()
def addCourse(request):
	if request.method == "POST":
		form = AddCourseForm(request.POST)		
		if form.is_valid():
			user = request.user
			canAddCourse = user.has_perm('stufacultyinfosys.add_course')
			facultyusername = request.POST['facultyusername']
			majorcode = request.POST['majorcode']
			major = Major.objects.get(pk=majorcode)
			coursename = request.POST['coursename']			
			coursenum = request.POST['coursenum']
			if facultyusername == user.username:
				try:
					faculty = Faculty.objects.get(username=facultyusername)
					course = Course.createCourse(coursenum, coursename, major, faculty)
					params = {
						'form':form,
						'canAddCourse':canAddCourse,
						'course':course,
						}			
					return render(request, 'stufacultyinfosys/addcourse.html', params)
				except IntegrityError as e:
					params = {
						'form' : form,
						'message' : e,
						}
					return render(request,'stufacultyinfosys/addcourse.html',params)
				
			else:
				message = "Incorrect username !"
				params = {
					'form':form,
					'message':message,
					'canAddCourse':canAddCourse,
					}
				return render(request, 'stufacultyinfosys/addcourse.html', params)
	else:
		user = request.user
		canAddCourse = user.has_perm('stufacultyinfosys.add_course')
		form = AddCourseForm()
		params = {
			'form':form,
			'canAddCourse':canAddCourse,
			}
		return render(request, 'stufacultyinfosys/addcourse.html', params)


@login_required()
def studenthome(request):
        return render(request, 'stufacultyinfosys/studenthome.html')


@login_required()
def registercourse(request):
	if request.method == "POST":
		form = RegisterCourseForm(request.POST)
		if form.is_valid():
			user = request.user
			majorcode = request.POST['majorcode']
			coursenum = request.POST['coursenum']
			course = Course.objects.get(pk=coursenum)
			try:
				student = Student.objects.get(username=user.username)
				course.student.add(student)
				course.save()
				params = {
					'form':form,
					'student':student,
					'course':course,
					}
				return render(request, 'stufacultyinfosys/registercourse.html', params)
			except Student.DoesNotExist:
				message = "You are not a student. You cannot register for a course."
				params = {
					'form':form,
					'message':message,
					}
				return render(request, 'stufacultyinfosys/registercourse.html', params)
	else:
		form = RegisterCourseForm()
		params = {
			'form':form,
			}
		return render(request, 'stufacultyinfosys/registercourse.html', params)


@login_required()
def listhome(request):
        return render(request, 'stufacultyinfosys/listhome.html')


def listfaculty(request):

	faculty_list = Faculty.objects.all()
	course_list = Course.objects.all()
	params = {
		'faculty_list':faculty_list,
		'course_list':course_list,
		}
	return render(request, 'stufacultyinfosys/listfaculty.html', params)


def liststudent(request):

	student_list = Student.objects.all()
	course_list = Course.objects.all()
	params = {
		'student_list':student_list,
		'course_list':course_list,
		}
	return render(request, 'stufacultyinfosys/liststudent.html', params)


def listcourse(request):

	course_list = Course.objects.all()
	params = {
		'course_list':course_list,
		}
	return render(request, 'stufacultyinfosys/listcourse.html', params)


