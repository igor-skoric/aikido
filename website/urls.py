from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('programs/', views.programs, name='programs'),
    path('instructors/', views.instructors, name='instructors'),
    path('instructor/<slug:slug>/', views.instructor, name='instructor'),
    path('locations/', views.locations, name='locations'),
    path('blog/', views.blog, name='blog'),
    path('masters/', views.masters, name='masters'),
    path('post/<slug:slug>/', views.post, name='post'),
    path('timeline/', views.timeline, name='timeline'),
    path('contact/', views.contact, name='contact'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('sitemap.xml', views.sitemap_xml, name='sitemap_xml'),
]
