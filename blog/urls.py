from django.urls import path


from .views import home_page_render,test,post_detail_render,add_like,add_comment,all_posts_render,dashboard_render_user,add_post,my_post_render,archive_post,delete_post,edit_post,delete_post_admin
 

urlpatterns = [
    path('',home_page_render,name='home_page'),
    path('kk/',test),
    path('post/<slug:slug>/',post_detail_render,name='post_detail'),
    path('post/<slug:slug>/like/',add_like,name='add_like'),
    path('post/<slug:slug>/comment/',add_comment,name='add_comment'),
    path('posts/',all_posts_render,name='all_posts_render'),
    path('dashboard/',dashboard_render_user,name='dashboard_render_user'),
    path('add_post/',add_post,name='add_post'),
    path('my_posts/',my_post_render,name='my_post_render'),
    path('post/archive/<slug:slug>/',archive_post,name='archive_post'),
    path('post/delete_post/<slug:slug>/',delete_post,name='delete_post'),
    path('post/edit_post/<slug:slug>/',edit_post,name='edit_post'),
    path('cadmin/delete_post_admin/<slug:slug>',delete_post_admin,name='delete_post_admin')
    
]
