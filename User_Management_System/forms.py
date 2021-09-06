from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Account, Csv
from django.core.validators import RegexValidator
from django.contrib.auth import authenticate

class UserRegisterForm(UserCreationForm):
    # email = forms.EmailField()
    # phone_regex = RegexValidator(regex=r'^\d{10,10}$', message = ("Phone number must be 10 digit number"))
    # phone_number = forms.CharField(validators=[phone_regex],  required=False)
    # choices = (
    #     ("Teacher", "Teacher"),
    #     ("Student", "Student"),)
    # user_type = forms.ChoiceField(choices=choices)
    # fullname = forms.CharField(max_length=30) 
    class Meta:
        model = Account
        fields = ['fullname', 'email','user_type','phone_number','supervisor', 'password1', 'password2','wlvid','project']

class AccountAuthenticationForm(forms.ModelForm):

	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	class Meta:
		model = Account
		fields = ('email', 'password')

	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Invalid login")

class csvmodelform(forms.ModelForm):
    class Meta:
        model = Csv
        fields =('file_name',)
