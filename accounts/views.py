from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import ValidationError
from django.views.decorators.cache import never_cache
from datetime import datetime, timedelta

import hashlib


from .forms import SignUpForm,LoginForm,NewPasswordForm
from .models import User,UserOtp,PasswordReset
from .services import gen_otp_six_digit,send_otp_email,send_password_reset
from blog.models import Post,Comment,PostLike


@never_cache
def otpverify(req):
    if req.session.get('cuuser',{}):
        return redirect('all_posts_render')
    if req.method == 'POST':
        user_email = req.session.get('no_verify_user',{})
        if not user_email:
            return HttpResponse("Expired Time Please Signup Again")
        try:
            user = User.objects.get(email=user_email)
        except:
            return HttpResponse("User Not Found")
        otp = UserOtp.objects.filter(user=user).order_by('-created_at').first()
        if not otp:
            return HttpResponse("Otp not found")
        if otp.is_expired():
            return HttpResponse("Otp Expired")
        else:
            getotp= str(req.POST.get('otp1'))+str(req.POST.get('otp2'))+str(req.POST.get('otp3'))+str(req.POST.get('otp4'))+str(req.POST.get('otp5'))+str(req.POST.get('otp6'))
            if getotp == otp.otp:
                user.is_active = True
                user.save()
                req.session['cuuser'] = {'useremail':user_email,"name":user.name,'user_profile':user.profile_image.url if user.profile_image else None}
                otp.delete()
                del req.session['no_verify_user']
                
                return redirect('all_posts_render')  
            else:
                return HttpResponse("Invalid Otp")  
            
    else:
        return render(req,'user/otpverify.html')
    

@never_cache
def signup(req):
    if req.session.get('cuuser',{}):
        return redirect('all_posts_render')
    form = SignUpForm()
    if req.method == 'POST':
        form = SignUpForm(req.POST)
        if form.is_valid():
            update = form.save(commit=False)
            raw_pass = form.cleaned_data.get('password').encode('utf-8')
            password = hashlib.sha256(raw_pass).hexdigest()
            update.password = password
            update.save()
            email = form.cleaned_data.get('email')
            user = User.objects.get(email=email)
            otp = gen_otp_six_digit()
            UserOtp.objects.create(otp=otp,user=user)
            send_otp_email(email, otp)
            req.session['no_verify_user'] = email
            
            
            return redirect('otpverify')
    return render(req,'user/signup.html',{'form':form})


@never_cache
def login(req):
    if req.session.get('cuuser',{}):
        return redirect('all_posts_render')
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
                    if user.is_active:
                        if user.is_blocked == False:
                            user = User.objects.get(email=email)
                            req.session['cuuser'] = {'useremail':email,"name":user.name,'user_profile':user.profile_image.url if user.profile_image else None}
                            if user.is_admin:
                                return redirect('admin_dashboard')
                            else:
                                return redirect('all_posts_render')
                        else:
                            return HttpResponse('Your Blocked By Admin')
                    else:
                        otp = gen_otp_six_digit()
                        UserOtp.objects.create(otp=otp,user=user)
                        send_otp_email(email, otp)
                        req.session['no_verify_user'] = email 
                        return redirect('otpverify')
                else:
                    form.add_error('password', 'Password Incorrect') 
            else:
                form.add_error('email', "email does't exists") 
    return render(req,'user/login.html',{'form':form})


def logout(request):
    request.session.flush()
    return redirect('login')

@never_cache
def user_edit(request,updated=False):
    user_session = request.session.get('cuuser', {})
    if user_session:
        if request.method == "POST":
            email = user_session['useremail']
            try:
                user = User.objects.get(email=email)
            except:
                return HttpResponse("User Not Found")
            name = request.POST.get('name')
            bio = request.POST.get('bio')
            profile_image = request.FILES.get('profile_image')
            if name and user.name != name :
                user.name = name
            
            if bio and user.bio != bio:
                user.bio = bio
            print(user.bio)
            if profile_image and user.profile_image != profile_image:
                user.profile_image = profile_image
            user.save()
            name = user.name
            bio = user.bio if user.bio else ""
            
            updated = True
            profile_image = user.profile_image.url if user.profile_image else ""
            request.session['cuuser'] = {'useremail':user.email,"name":user.name,'user_profile':user.profile_image.url if user.profile_image else None}
            return render(request,'user/user_edit.html',{'cuuser':user_session,'name':name,'bio':bio,'profile_image':profile_image,'updated':updated})  
                
        else:
            
            email = user_session['useremail']
            try:
                user = User.objects.get(email=email)
            except:
                return HttpResponse("User Not Found")
            name = user.name
            bio = user.bio if user.bio else ""
            profile_image = user.profile_image.url if user.profile_image else ""
        
    else:
        return redirect('login')
    return render(request,'user/user_edit.html',{'cuuser':user_session,'name':user,'bio':bio,'profile_image':profile_image,'updated':updated})


@never_cache
def forget_password(request):
    
    response = render(request,'user/forget_password.html')
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                obj = PasswordReset(user=user)
                obj.save()
                link = f"http://127.0.0.1:8000/reset-password/?token={obj.token}"
                send_password_reset(email,link)
                return render(request,'user/emailsend.html')
            else:
                response = render(request,'user/forget_password.html',{'error':'Email not found in our database'})
                print('hi')
        else:
            response = render(request,'user/forget_password.html',{'error':'Enter a valid emial'})
    return response
    
@never_cache
def reset_password(request):
    response = render(request,'user/new_password.html')
    if request.method == 'POST':
        
        token = request.POST.get('token')
        
        if PasswordReset.objects.filter(token=token).exists():
            
            token_obj = PasswordReset.objects.get(token=token)
            print(token_obj.is_expired())
            if token_obj.is_expired():
                
                user = token_obj.user
                form = NewPasswordForm(request.POST)
                print('valid',form.is_valid())
                if form.is_valid():
                    
                    raw_pass = form.cleaned_data.get('password').encode('utf-8')
                    password = hashlib.sha256(raw_pass).hexdigest()
                    user.password = password
                    user.save()
                    token_obj.delete()
                    response = render(request,'user/password_reset_succ.html')
                else:
                    
                    response = render(request,'user/new_password.html',{'error':form.errors})
            else:
                response = render(request,'user/token_expired.html')
        else:
            response = render(request,'user/token_expired.html')
    return response

@never_cache
def admin_dashboard(request):
    user_session = request.session.get('cuuser', {})    
    if user_session:
        user = User.objects.get(email = user_session['useremail'])
        if user.is_admin:
            user_count = User.objects.all().count()
            post_count = Post.objects.all().count()
            comment_count = Comment.objects.all().count()
            likes_count = PostLike.objects.all().count()
            return render(request,'admin/admin_dashboard.html',{'user_count':user_count,'post_count':post_count,'comment_count':comment_count,'likes_count':likes_count,'current':'admin_dashboard'})
        else:
            return HttpResponse("Only Admin Can Access")
    else:
        return redirect('login')
    
@never_cache
def user_management(request):
    user_session = request.session.get('cuuser', {})    
    if user_session:
        user = User.objects.get(email = user_session['useremail'])
        if user.is_admin:
            users = User.objects.all()
            return render(request,'admin/user_management.html',{'users':users,'current':'user_mana'})
        else:
            return HttpResponse("Only Admin Can Access")
    else:
        return redirect('login')
    
    
def delete_user(request,id):
    user_session = request.session.get('cuuser', {})    
    if user_session:
        user = User.objects.get(email = user_session['useremail'])
        if user.is_admin:
            if User.objects.filter(id=id).exists():
                user = User.objects.get(id=id)
                user.delete()
                return redirect('user_management')
            else:
                return HttpResponse("user Not found")
        else:
            return HttpResponse("Only Admin Can Access")
    else:
        return redirect('login')
    

def block_user(request,id):
    user_session = request.session.get('cuuser', {})    
    if user_session:
        user = User.objects.get(email = user_session['useremail'])
        if user.is_admin:
            if User.objects.filter(id=id).exists():
                user = User.objects.get(id=id)
                if user.is_blocked:
                    user.is_blocked = False
                else:
                    user.is_blocked = True
                
                user.save()
                return redirect('user_management')
            else:
                return HttpResponse("user Not found")
        else:
            return HttpResponse("Only Admin Can Access")
    else:
        return redirect('login')
    
@never_cache
def posts_management(request):
    user_session = request.session.get('cuuser', {})    
    if user_session:
        user = User.objects.get(email = user_session['useremail'])
        if user.is_admin:
            posts = Post.objects.all()
            return render(request,'admin/manage_posts.html',{'posts':posts,'current':'posts_mana'})
        else:
            return HttpResponse("Only Admin Can Access")
    else:
        return redirect('login')
    
    
    
    