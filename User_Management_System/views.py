from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from Feedback_Management_System.models import *
from .models import Account, Csv
import csv
from .forms import UserRegisterForm , AccountAuthenticationForm, csvmodelform
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required




# from django.template.loader import render_to_string
# from weasyprint import HTML
# import tempfile
# Create your views here.


def home(request):
	user = request.user
	if user.is_authenticated:
		if user.check_password('herald@1234'):
			return redirect ('logout')
		else:
			if user.user_type != 'Student':
				return redirect ('listuser', 'student')
			else:
				return redirect ('stdmg', user.id)

def listuser(request, usertype):
	user = request.user
	if user.is_admin:
		if usertype == 'teacher':
			i = Account.objects.filter(user_type='Teacher').order_by('fullname')
			return render (request, 'UMS/listuser.html', {'nbar': 'Teacher', 'account': i} )
		else:
			i = Account.objects.filter(user_type='Student').order_by('fullname')
			t = Account.objects.filter(user_type='Teacher').order_by('fullname')
			g = markingGrids.objects.all().order_by('id')
			return render (request, 'UMS/listuser.html', {'nbar': 'Student', 'account': i, 'teachers':t, 'g':g} )
	elif  user.user_type == 'Teacher':
		i = Account.objects.filter(supervisor=user.fullname)
		g = markingGrids.objects.all().order_by('id')
		print('supervisor')
		return render (request, 'UMS/listuser.html', {'nbar': 'Student', 'account': i, 'g':g} )



	
def login_view(request):


	user = request.user
	if user.is_authenticated:
		if user.check_password('herald@1234'):
			return render(request, 'UMS/Changepwd.html')
		else:
			return redirect("home")
	
		

	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)

			if user:
				if user.check_password('herald@1234'):
					login(request, user)
					return render(request, 'UMS/changepwd.html')
				else:
					login(request, user)
					return redirect("home")

	else:
		form = AccountAuthenticationForm()
	return render(request, "UMS/login.html", {'form':form})


def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			type = form.cleaned_data.get('user_type')
			messages.success(request, f'Account created for {username}!')
			if type == 'Teacher':
				return redirect('/listuser/teacher/')
			else:
				return redirect('/listuser/student/')
	else:
		form = UserRegisterForm()
		i = Account.objects.filter(user_type='Teacher')

	return render(request, 'UMS/register.html', {'form': form, "teachers": i })


def logout_view(request):
	logout(request)
	return redirect('login')



@login_required
def pwdchange(request):
	if request.method == 'POST':

		password1 = request.POST.get('pwd1')
		password2 = request.POST.get('pwd2')

		if password1 == password2:
			user = request.user
			user.set_password(password1)
			user.save()
			return redirect ('logout')
		else:
			return render(request, 'UMS/Error.html', {'message':'Password Change failed. Try again'})

def delete(request, id):
	i = Account.objects.get(id=id)
	type = i.user_type
	i.delete()
	if type == 'Teacher':
		return redirect('/listuser/teacher/')
	else:
		return redirect('/listuser/student/')

def update(request, id):
	i = Account.objects.get(id = id)
	if request.method == 'POST':
		i.fullname = request.POST.get('name')
		i.email = request.POST.get('email')
		i.phone_number = request.POST.get('phone_number')
		i.supervisor = request.POST.get('supervisor')
		i.wlvid = request.POST.get('wlvid')
		i.project = request.POST.get('project')
		i.save()
	
	if i.user_type == 'Student':
		return redirect ('/listuser/student/')
	else:
		return redirect ('/listuser/teacher/')
	
def resetpwd(request, id):
	i = Account.objects.get(id=id)
	type = i.user_type
	i.set_password('herald@1234')
	i.save()
	if type == 'Teacher':
		return redirect('/listuser/teacher/')
	else:
		return redirect('/listuser/student/')

def uploadfileview(request):
	form = csvmodelform(request.POST or None, request.FILES or None)
	if form.is_valid():
		form.save()
		form = csvmodelform()
		obj = Csv.objects.get(activated=False)
		with open(obj.file_name.path, 'r') as f:
			reader = csv.reader(f)

			for i, row in enumerate(reader):
				if i==0:
					pass
				else:
					fullname = row[0].upper()
					email = row[1]
					type = row[2]
					phone = row[3]
					supervisor = row[4].upper()
					wlvid = row[5]
					project = row[6]
					print (fullname, email, type, phone, supervisor, wlvid, project)
					user= Account.objects.create_user(email = email, fullname=fullname, password ='herald@1234' )
					user.save()
					u = Account.objects.get(email=email)
					u.user_type = type
					u.phone_number = phone
					u.supervisor = supervisor
					u.wlvid = wlvid
					u.project = project
					u.save()
			obj.activated = True
			obj.save()	
			return render(request, 'UMS/upload.html', {'form':form, 'message':'Users Added Successfully'}) 
	return render(request, 'UMS/upload.html', {'form':form}) 

