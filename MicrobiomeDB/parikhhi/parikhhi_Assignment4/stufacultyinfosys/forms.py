from django import forms
from models import Major, Course

class LoginForm(forms.Form):
	
	username = forms.CharField(max_length=20)
	password = forms.CharField(widget=forms.PasswordInput(), max_length=20)
	

class RegisterForm(forms.Form):

	USERTYPE_CHOICES = (
		("Faculty",'Faculty'),
		("Student",'Student'),
	)

	firstname = forms.CharField(max_length=50)
	lastname = forms.CharField(max_length=50)
	majorcode = forms.ModelChoiceField(queryset=Major.objects.all())
	usertype = forms.ChoiceField(choices=USERTYPE_CHOICES)
	useremail = forms.EmailField()
	username = forms.CharField(max_length=20)
	password1 = forms.CharField(widget=forms.PasswordInput(), max_length=20)
	password2 = forms.CharField(widget=forms.PasswordInput(), max_length=20)


class AddMajorForm(forms.Form):

	facultyusername = forms.CharField(max_length=20)
	majorcode = forms.CharField(max_length=4)
	majorfullname = forms.CharField(max_length=100)

	
class AddCourseForm(forms.Form):

	facultyusername = forms.CharField(max_length=20)
	majorcode = forms.ModelChoiceField(queryset=Major.objects.all())
	coursename = forms.CharField(max_length=50)	
	coursenum = forms.CharField(max_length=10)	


class RegisterCourseForm(forms.Form):

	majorcode = forms.ModelChoiceField(queryset=Major.objects.all())
	coursenum = forms.ModelChoiceField(queryset=Course.objects.all())


