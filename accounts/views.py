from django.shortcuts import render
from django.http import HttpResponse
from django.forms import ValidationError


import hashlib


from .forms import SignUpForm,LoginForm
from .models import User




def signup(req):
    if req.session.get('user',{}):
        return HttpResponse('Already have')
    form = SignUpForm()
    if req.method == 'POST':
        form = SignUpForm(req.POST)
        if form.is_valid():
            update = form.save(commit=False)
            raw_pass = form.cleaned_data.get('password').encode('utf-8')
            password = hashlib.sha256(raw_pass).hexdigest()
            update.password = password
            update.save()
            req.session['user'] = {'useremail':form.cleaned_data.get('email'),"name":form.cleaned_data.get('name')}
            return HttpResponse("Finish")
    
    
    return render(req,'user/signup.html',{'form':form})


def login(req):
    if req.session.get('user',{}):
        return HttpResponse('Already have')
    form = LoginForm()
    if req.method == 'POST':
        form = LoginForm(req.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                raw_pass = form.cleaned_data.get('password').encode('utf-8')
                password = hashlib.sha256(raw_pass).hexdigest()
                if user.password == password:
                    req.session['user'] = {'useremail':email,"name":user.name}
                    return HttpResponse('Login Succsesfull')
                else:
                    form.add_error('password', 'Password Incorrect') 
            else:
                form.add_error('email', "email does't exists") 
                    
                
            
           
        
    
    
    return render(req,'user/login.html',{'form':form})
    