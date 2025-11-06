from django import forms
from django.forms import ValidationError


from .models import User


class SignUpForm(forms.ModelForm):
    
    
    class Meta():
        model = User
        fields = ['name','email','password']
        widgets = {
            "name":forms.TextInput(attrs={'class':'form-input block w-full rounded-lg border border-[#d0dce7] dark:border-gray-700 bg-slate-50 dark:bg-gray-800 h-14 pl-12 pr-4 text-base text-[#0e151b] dark:text-slate-50 placeholder:text-gray-400 dark:placeholder:text-gray-500 focus:outline-none','placeholder':'Enter Your FullName'}),
            "email":forms.TextInput(attrs={'class':'form-input block w-full rounded-lg border border-[#d0dce7] dark:border-gray-700 bg-slate-50 dark:bg-gray-800 h-14 pl-12 pr-4 text-base text-[#0e151b] dark:text-slate-50 placeholder:text-gray-400 dark:placeholder:text-gray-500 focus:outline-none','placeholder':'Enter Your Email'}),
            "password":forms.PasswordInput(attrs={'class':'form-input block w-full rounded-lg border border-[#d0dce7] dark:border-gray-700 bg-slate-50 dark:bg-gray-800 h-14 pl-12 pr-4 text-base text-[#0e151b] dark:text-slate-50 placeholder:text-gray-400 dark:placeholder:text-gray-500 focus:outline-none','placeholder':'Enter Your Password'})
            
        }
        
        
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 4:
            raise ValidationError("Name must be at least 3 characters")
        for i in name:
            if i.isalpha():
                continue
            elif i == " ":
                continue
            else:
                raise ValidationError("Name must contain only letters and spaces")
        return name
    
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        message = ""
        if " " in password:
            message += "not include space"
        for i in password:
            if i.isupper():
                break
        else:
            message += "The title must contain at least one uppercase letter.\n" 
        for i in password:
            if i in [ '@', '_','!','#','$','%','^','&','*','(',')','<','>','?','~']:
                break
        else:
            message += "Must Include a Special Character\n"
        for i in password:
            if i.isdigit():
                break 
        else:
            message += "Must Include a Special Character\n"
        if len(password) < 8:
            message += "Must 8 Characters"
        if message:
            raise ValidationError(message)
        return password
    
    
    
class LoginForm(forms.Form):
    email = forms.EmailField(widget =forms.EmailInput(attrs={
        'class':'form-input block w-full rounded-lg border border-[#d0dce7] dark:border-gray-700 bg-slate-50 dark:bg-gray-800 h-14 pl-12 pr-4 text-base text-[#0e151b] dark:text-slate-50 placeholder:text-gray-400 dark:placeholder:text-gray-500 focus:outline-none','placeholder':'Enter Your Email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-input block w-full rounded-lg border border-[#d0dce7] dark:border-gray-700 bg-slate-50 dark:bg-gray-800 h-14 pl-12 pr-4 text-base text-[#0e151b] dark:text-slate-50 placeholder:text-gray-400 dark:placeholder:text-gray-500 focus:outline-none','placeholder':'Enter Your Password'
    }))
    
             


class NewPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())
            
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        message = ""
        for i in password:
            if i.isupper():
                break
        else:
            message += "The title must contain at least one uppercase letter.\n" 
        for i in password:
            if i in [ '@', '_','!','#','$','%','^','&','*','(',')','<','>','?','~']:
                break
        else:
            message += "Must Include a Special Character\n"
        for i in password:
            if i.isdigit():
                break 
        else:
            message += "Must Include a Special Character\n"
        if len(password) < 8:
            message += "Must 8 Characters"
        if message:
            raise ValidationError(message)
        return password
            
            