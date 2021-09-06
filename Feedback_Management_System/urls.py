from django.urls import path
from . import views

urlpatterns = [
    path ('', views.grid, name='grid'),
    path('criterias/<int:id>/', views.criteria, name='criteria'),
    path('descriptions/<int:id>/', views.description, name='description'),
    path('updategrid/<int:id>/', views.updategrid, name='updategrid'),
    path('deletegrid/<int:id>/', views.deletegrid, name='deletegrid'),
    path('addgrid/', views.addgrid, name='addgrid'),
    path('updatecriteria/<int:id>/', views.updatecriteria, name='updatecriteria'),
    path('deletecriteria/<int:id>/', views.deletecriteria, name='deletecriteria'),
    path('addcriteria/<int:id>/', views.addcriteria, name='addcriteria'),
    path('deletedescription/<int:id>/', views.deletedescription, name='deletedescp'),
    path('editdescription/<int:id>/<int:cid>/', views.editdescription, name='editdescp'),
    path('adddescription/<int:id>/', views.adddescription, name='adddescp'),
    path('addcomment/', views.addcomment, name='addcmnt'),
    path('addmarks/', views.addmarks, name='addmarks'),
    path('commentdel/', views.cmtdel, name='cmtdel'),
    
]