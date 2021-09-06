

from django.urls import path

from . import views
from django.contrib.auth import views as auth_views
from Feedback_Management_System.views import studentmarkinggrid
from Report_Management_System.views import report , downloadpdf

# for password reset to work through email you must turn on less secure apps feature on your gmail account https://www.youtube.com/redirect?q=https%3A%2F%2Fmyaccount.google.com%2Flesssecureapps&redir_token=QUFFLUhqbmxMOExtOEZNbWU0MW0wMm1paklSeXB6MEduQXxBQ3Jtc0tuelhKRVZaMEZpZHgtYl9qbU1mNjdTYll0SHFOS0pjSkxwYWs4VHJubjJjOWY3RWM5UnY3SFpXa28zckhwWWFiMDFnTV9vZVZnNDZnWThLZ3E0ZGlBX2t4dU5IR0tiTHRFT21EUVNaS21YMkJKQnlJZw%3D%3D&v=sFPcd6myZrY&event=video_description

urlpatterns = [

    path('register/', views.register, name='register' ),
    path('home/', views.home, name='home' ),
    path('pwdchange/', views.pwdchange, name='pwdchange' ),
    path('listuser/<str:usertype>/', views.listuser, name='listuser'),
    path('resetpwd/<int:id>/', views.resetpwd, name='resetpwd'),
    path('delete_user/<int:id>/', views.delete, name='delete_user'),
    path('update_details/<int:id>/', views.update, name='update_user'),
    path('studentmarkinggrid/<int:id>/', studentmarkinggrid, name='stdmg'),
    path('report/<int:id>/<str:gridtitle>/', report, name='report'),
    path('pdf/', downloadpdf, name='downloadpdf'),


    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="UMS/password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="UMS/password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="UMS/password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="UMS/password_reset_done.html"), 
        name="password_reset_complete"),

    path('uploadfile/',views.uploadfileview, name='fileupload')    
]
