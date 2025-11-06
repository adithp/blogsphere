from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.decorators.cache import never_cache



from .models import Post,LatestPost,Comment,PostLike,Category
from accounts.models import User
from .forms import PostForm


@never_cache
def home_page_render(request):
    
    posts = LatestPost.objects.filter(is_archived=False)[:6]
    print(posts)
    return render(request,'blog/home.html',{'posts':posts})

@never_cache
def all_posts_render(request):
    
    search = request.GET.get('search',' ')
    category_from = request.GET.get('category','')
    caties = Category.objects.all()
    cat = caties[:3]
    page = request.GET.get('page','')
    if search and category_from:
        try:
            categoryobj = Category.objects.get(title=category_from) 
        except:
            pass
        if category_from:  
            before_posts = Post.objects.filter(category=categoryobj).filter(Q(title__icontains=search) | Q(content__icontains=search)).filter(is_archived=False)
            paginator = Paginator(before_posts,6)
            if page:
                posts = paginator.get_page(int(page))
            else:
                posts = paginator.get_page(1)
    elif category_from:
        try:
            categoryobj = Category.objects.get(title=category_from) 
        except:
            return HttpResponse("No Category Found")
        before_posts = Post.objects.filter(category=categoryobj,is_archived=False)
        paginator = Paginator(before_posts,6)
        if page:
            posts = paginator.get_page(int(page))
        else:
            posts = paginator.get_page(1)
    elif search:
        before_posts = Post.objects.filter((Q(title__icontains=search) | Q(content__icontains=search) & Q(is_archived = False)))
        paginator = Paginator(before_posts,6)
        if page:
            posts = paginator.get_page(int(page))
        else:
            posts = paginator.get_page(1)
    else:
        before_posts = LatestPost.objects.filter(is_archived = False)
        paginator = Paginator(before_posts,6)
        if page:
            posts = paginator.get_page(int(page))
        else:
            posts = paginator.get_page(1)
    return render(request,'blog/allposts.html',{'posts':posts,'search':search,'categories':cat,'page': page if page else 1,'total_pages':paginator.num_pages,'caties':caties})

@never_cache
def post_detail_render(request,slug):
    user_session = request.session.get('cuuser', {})
    if Post.objects.filter(slug=slug,is_archived = False).exists():
        
        post = Post.objects.get(slug=slug)
        comments = Comment.objects.filter(post=post)
        if user_session:
            email = user_session['useremail']
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                is_liked = PostLike.objects.filter(post=post,user=user).exists()
            else:
                is_liked = False
        else:
            is_liked = False     
        return render(request,'blog/post_detail.html',{'post':post,'comments':comments,'is_liked':is_liked})
    else:
        return HttpResponse('post not found')
    

def add_like(request,slug):
    user_session = request.session.get('cuuser', {})
    if user_session and User.objects.filter(email = user_session['useremail']):
        
        user = User.objects.get(email = user_session['useremail'])
        if Post.objects.filter(slug=slug).exists():
            post = Post.objects.get(slug=slug)
            if  PostLike.objects.filter(user=user,post=post).exists():
                postLike = PostLike.objects.get(user=user,post=post)
                postLike.delete()
                post.likes_count -= 1
                post.save()
                return redirect('post_detail',slug)
            else:
                PostLike.objects.create(user=user,post=post)
                post.likes_count +=1
                post.save()
                return redirect('post_detail',slug)
        else:
            return HttpResponse("Post Not Found")
        
    else:
        return redirect('login')
    
@never_cache   
def add_comment(request,slug):
    user_session = request.session.get('cuuser', {})
    if user_session and User.objects.filter(email = user_session['useremail']):
        
        user = User.objects.get(email = user_session['useremail'])
        if Post.objects.filter(slug=slug).exists():
            post = Post.objects.get(slug=slug)
            content = request.POST.get('content')
            Comment.objects.create(post=post,user=user,content=content)
            post.comment_count += 1
            post.save()
            return redirect('post_detail',slug)
        else:
            return HttpResponse("Post Not Found")
    else:
        return redirect('login')
    
@never_cache
def dashboard_render_user(request):
    user_session = request.session.get('cuuser', {})
    if user_session and User.objects.filter(email = user_session['useremail']):
        user = User.objects.get(email = user_session['useremail'])
        posts = Post.objects.filter(author=user)
        total_likes_count = 0
        total_comments_count = 0
        for post in posts:
            total_likes_count += post.likes_count
            total_comments_count += post.comment_count
        posts_count = posts = Post.objects.filter(author=user).count()
        
        
        return render(request,'blog/dashboard.html',{'total_like':total_likes_count,'total_posts':posts_count,'total_comment':total_comments_count})
    else:
        return redirect('login')
        
@never_cache
def add_post(request):
    user_session = request.session.get('cuuser', {})
    if user_session:
        form = PostForm()
        categories = Category.objects.all()
        if request.method == 'POST':
            user = User.objects.get(email = user_session['useremail'])
        
            
            if categories.filter(title = request.POST.get('category')).exists():
                catt = categories.get(title = request.POST.get('category'))
            else:
                catt = Category(title=request.POST.get('category'))
                catt.save()
            form = PostForm(request.POST,request.FILES)
            print(form.is_valid())
            print(form.errors)
            if form.is_valid():
                
                
                commit = form.save(commit=False)
                commit.category = catt
                commit.author = user
                commit.save()
                return redirect('dashboard_render_user')
                    
                
        return render(request,'blog/add_post.html',{'form':form,'categories': categories })
    else:
        return redirect('login')
    
@never_cache
def my_post_render(request):
    user_session = request.session.get('cuuser', {})    
    if user_session:
        user = User.objects.get(email = user_session['useremail'])
        posts = Post.objects.filter(author=user)
        return render(request,'blog/my_posts.html',{'posts':posts})
    else:
        return redirect('login')
 
@never_cache   
def archive_post(request,slug):
    user_session = request.session.get('cuuser', {})    
    if user_session:
        if Post.objects.filter(slug=slug).exists():
            user = User.objects.get(email = user_session['useremail'])
            post = Post.objects.get(slug=slug)
            if post.author == user:
                if post.is_archived:
                    post.is_archived = False
                else:
                    post.is_archived = True
                post.save()
                return redirect('my_post_render')
            else:
                return redirect('login') 
                   
        else:
            return HttpResponse("Post Not Found")
        
    else:
        return redirect('login')
    
    
def delete_post(request,slug):
    user_session = request.session.get('cuuser', {})    
    if user_session:
        if Post.objects.filter(slug=slug).exists():
            user = User.objects.get(email = user_session['useremail'])
            post = Post.objects.get(slug=slug)
            if post.author == user:
                post.delete()
                print(request.path)
                return redirect('my_post_render')
            else:
                return redirect('login') 
        else:
            return HttpResponse("Post Not Found")
    return redirect('login')


def delete_post_admin(request,slug):
    
    user_session = request.session.get('cuuser', {})    
    if user_session:
        if Post.objects.filter(slug=slug).exists():
            
            user = User.objects.get(email = user_session['useremail'])
            if user.is_admin:
                
                post = Post.objects.get(slug=slug)
               
                
                post.delete()
                return redirect('posts_management')
                
            else:
                return HttpResponse('only admin and post user can do')
        else:
            return HttpResponse("Post Not Found")
    return redirect('login')
        
        
    

@never_cache
def edit_post(request,slug):
    user_session = request.session.get('cuuser', {})
    if user_session:
        user = User.objects.get(email = user_session['useremail'])
        if Post.objects.filter(slug=slug).exists():
            post = Post.objects.get(slug=slug)
            if post.author == user:
                categories = Category.objects.all()
                if request.method == 'POST':
                    if categories.filter(title = request.POST.get('category')).exists():
                        catt = categories.get(title = request.POST.get('category'))
                    else:
                        catt = Category(title=request.POST.get('category'))
                        catt.save()
                    form = PostForm(request.POST,request.FILES,instance=post)
                    print(form.is_valid())
                    print(form.errors)
                    if form.is_valid():
                        
                        
                        commit = form.save(commit=False)
                        commit.category = catt
                        commit.author = user
                        commit.save()
                        return redirect('dashboard_render_user')
                post = Post.objects.get(slug=slug)
                form = PostForm(instance=post)
                return render(request,'blog/add_post.html',{'form':form,'categories': categories }) 
            else:
                return redirect('login')
        else:
            return HttpResponse("Post Not Found")      
        
    else:
        return redirect('login')



def test(req):
    post = Post.objects.first()
    
    return render(req,'blog/test.html',{'post':post})
    