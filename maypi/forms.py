from django import forms
from django.contrib.auth.models import User
from django.conf import settings
from maypi.models import DoorCode

class UserForm(forms.Form):
	first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'class':'form-control'}))
	last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'class':'form-control'}))
	email = forms.EmailField(label="E-mail", max_length=75, widget=forms.TextInput(attrs={'class':'form-control'}))
	
	def save(self):
		if not self.is_valid(): raise forms.ValidationError('The form is not valid')
		first = self.cleaned_data['first_name'].strip().title()
		if len(first) == 0: raise forms.ValidationError("First Name Required.")
		last = self.cleaned_data['last_name'].strip().title()
		if len(last) == 0: raise forms.ValidationError("Last Name Required.")
		username = "%s_%s" % (first.lower(), last.lower())
		if User.objects.filter(username=username).count() > 0: raise forms.ValidationError("Username '%s' is already in use." % username)
		email = self.cleaned_data['email'].strip().lower()
		if len(email) == 0: raise forms.ValidationError("Email Required.")
		if User.objects.filter(email=email).count() > 0: raise forms.ValidationError("That email address is already in use.")
		# Notice there is no password gatherd.  They shouldn't ever need to log in so they don't need a password.
		user = User(username=username, first_name=first, last_name=last, email=email)
		user.save()		
		return user
		
class DoorCodeForm(forms.ModelForm):
	def clean_code(self):
		data = self.cleaned_data['code']
		if not data.isdigit(): raise forms.ValidationError("Code must be a number.")
		if len(data) < 5: raise forms.ValidationError("Code must be at least 5 digits.")
		door_code = DoorCode.objects.filter(code=data).first()
		if door_code: raise forms.ValidationError("Code already in use")
		return data
		
	def save(self):
		if not self.is_valid(): raise forms.ValidationError('The form is not valid')
		user = self.cleaned_data['user']
		code = self.cleaned_data['code']
		start = self.cleaned_data['start']
		end = self.cleaned_data['end']
		door_code = DoorCode(user=user, code=code, start=start, end=end)
		door_code.save()
		return door_code
	
	class Meta:
		model = DoorCode
		fields = ['user', 'code', 'start', 'end']
		widgets = { 
			'code': forms.TextInput(attrs={'class':'form-control'}),
			'start': forms.DateTimeInput(attrs={'class':'datepicker form-control'}),
			'end': forms.DateTimeInput(attrs={'class':'datepicker form-control'}),
		}
	