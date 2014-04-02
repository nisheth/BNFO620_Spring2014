# Create your models here.

from django.db import models
import sys


class Major(models.Model):
	id = models.AutoField(primary_key=True)
	majorcode = models.CharField(max_length=4, unique=True)
	majorfullname = models.CharField(max_length=100)

	def __unicode__(self):
		return self.majorcode
	
	@classmethod
	def createMajor(cls, majorcode, majorfullname):
		major = Major(majorcode=majorcode, majorfullname=majorfullname)
		major.save()
		return major


class Faculty(models.Model):
	id = models.AutoField(primary_key=True)
	firstname = models.CharField(max_length=50)
	lastname = models.CharField(max_length=50)
	useremail = models.EmailField()
	username = models.CharField(max_length=20, unique=True)
	password = models.CharField(max_length=50)
	major = models.ForeignKey(Major)
	
	def __unicode__(self):
		return self.username

	@classmethod
	def createFaculty(cls, firstname, lastname, useremail, username, password, major):
		faculty = Faculty(firstname=firstname, lastname=lastname, useremail=useremail, username=username, password=password, major=major)
		faculty.save()
		return faculty


class Student(models.Model):
	id = models.AutoField(primary_key=True)
	firstname = models.CharField(max_length=50)
	lastname = models.CharField(max_length=50)
	useremail = models.EmailField()
	username = models.CharField(max_length=20, unique=True)
	password = models.CharField(max_length=50)
	major = models.ForeignKey(Major)
	
	def __unicode__(self):
		return self.username

	@classmethod
	def createStudent(cls, firstname, lastname, useremail, username, password, major):
		student = Student(firstname=firstname, lastname=lastname, useremail=useremail, username=username, password=password, major=major)
		student.save()
		return student


class Course(models.Model):
	id = models.AutoField(primary_key=True)
	coursename = models.CharField(max_length=50)
	coursenum = models.CharField(max_length=10, unique=True)
	major = models.ForeignKey(Major)
	faculty = models.ForeignKey(Faculty)
	student = models.ManyToManyField(Student, null=True)	
	
	def __unicode__(self):
		return self.coursenum
	
	@classmethod
	def createCourse(cls, coursenum, coursename, major, faculty):
		course = Course(coursenum=coursenum, coursename=coursename, major=major, faculty=faculty)
		course.save()
		return course



