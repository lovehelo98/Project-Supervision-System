from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator

# Create your models here.


class MyAccountManager(BaseUserManager):
	def create_user(self, email, fullname, password=None):
		if not email:
			raise ValueError('Users must have an email address')
		if not fullname:
			raise ValueError('Users must have a fullname')

		user = self.model(
			email=self.normalize_email(email),
			fullname=fullname,
			
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, fullname, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			fullname=fullname,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class Account(AbstractBaseUser):
	email 					= models.EmailField(verbose_name="email", max_length=60, unique=True)
	date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin				= models.BooleanField(default=False)
	is_active				= models.BooleanField(default=True)
	is_staff				= models.BooleanField(default=False)
	is_superuser			= models.BooleanField(default=False)
	phone_regex = RegexValidator(regex=r'^\d{10,10}$', message="Phone number must be 10 digits")
	phone_number = models.CharField(validators=[phone_regex], max_length=10, blank=True)
	fullname				= models.CharField(max_length=30)
	supervisor  = models.CharField(max_length=30, blank=True)
	choices = (
	("Teacher", "Teacher"),("Student", "Student"),)
	user_type = models.CharField(max_length=30, choices=choices)
	wlvid = models.CharField(max_length=8, blank=True)
	project = models.CharField(max_length=30, blank=True , null=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['fullname',]

	objects = MyAccountManager()

	def __str__(self):
		return self.email

# For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
		return self.is_admin

# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True



class Csv(models.Model):
	file_name = models.FileField(upload_to='csvs')
	uploaded = models.DateTimeField(auto_now_add=True)
	activated = models.BooleanField(default=False)

	def __str__(self):
		return f"File id: {self.id}"