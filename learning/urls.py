from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('courses/', views.courses, name='courses'),
    path('create/', views.create, name='create'),
    path('course-detail/<int:course_id>/', views.course_detail, name='course-detail'),
    path('enroll/<int:course_id>/', views.enroll, name='enroll'),
    path('add-lesson/', views.add_lesson, name='add_lesson'),
    path('events/', views.events, name='events'),
    path('contact/', views.contact, name='contact'),
    path('pricing/<int:course_id>/', views.pricing, name='pricing'),
    path('create-course/', views.create_course, name='create_course'),
    path('trainers/', views.trainers, name='trainers'),
    path('trainer_details/', views.trainer_details, name='trainer_details'),
]
