from django.urls import path


from . import views


urlpatterns = [
    path('login/',views.login,name='login'),
    path('signup/',views.signup,name='signup'),
    path('logout/',views.logout,name='logout'),
    path('verify_otp/',views.otpverify,name='otpverify'),
    path('user_edit/',views.user_edit,name='user_edit'),
    path('forget_password/',views.forget_password,name='forget_password'),
    path('reset-password/',views.reset_password,name='reset_password'),
    path('cadmin/dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('cadmin/user_management/',views.user_management,name='user_management'),
    path('cadmin/delete_user/<uuid:id>/',views.delete_user,name='delete_user'),
    path('cadmin/block_user/<uuid:id>/',views.block_user,name='block_user'),
    path('cadmin/posts_management/',views.posts_management,name='posts_management')
]