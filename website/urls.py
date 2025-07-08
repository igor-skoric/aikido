from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('programs/', views.programs, name='programs'),
    path('instructors/', views.instructors, name='instructors'),
    path('instructor/<str:slug>', views.instructor, name='instructor'),
    path('locations/', views.locations, name='locations'),
    path('blog/', views.blog, name='blog'),
    path('masters/', views.masters, name='masters'),
    path('post/<str:slug>', views.post, name='post'),
    path('shop/', views.shop, name='shop'),
    path('single-product/<str:slug>', views.product, name='product'),
    path('timeline/', views.timeline, name='timeline'),
    path('contact/', views.contact, name='contact'),
]
