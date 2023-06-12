import json
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import JsonResponse
from .models import *
from math import ceil
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user
from django.contrib.auth.models import User
from .models import *
from django.shortcuts import render, get_object_or_404
from django.conf import settings
import os


def index(request):
    new = ""
    login_status = ""
    USR = ""

    if request.method == "POST":
        if "loginForm" in request.POST:
            userID = request.POST.get("UserID", "")
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            userType = request.POST.get('userType', '')
            if userType == 'student':
                try:
                    student = User.objects.get(username=username)
                    if student.password == password:
                        new = username
                        print(new, " has logged in as a user or student")
                        login_status = "success"
                    else:
                        print("wrong password by user")
                        login_status = "wrong_password"
                except User.DoesNotExist:
                    print("user not registered")
                    login_status = "not_registered"
            elif userType == 'trainer':
                try:
                    trainer = Trainer.objects.get(username=username)
                    if trainer.password == password:
                        new = username
                        print(new, " has logged in as a trainer")
                        login_status = "success"
                    else:
                        print("wrong password by trainer")
                        login_status = "wrong_password"
                except Trainer.DoesNotExist:
                    print("this trainer doesn't exist")
                    login_status = "not_registered"
            # Return JSON response
            return JsonResponse({'login_status': login_status, 'new': new})

        elif "signupForm" in request.POST:
            # Process signup form
            choice = request.POST.get('userType', '')
            print("the choice is: ", choice)
            if (choice == "student"):
                Name = request.POST.get('Name', '')
                print(Name)
                email = request.POST.get('email', '')
                print(email)
                username = request.POST.get('username', '')
                password = request.POST.get('Password', '')
                contact = request.POST.get('contact', '')
                print("user data saved")
                user = User(Name=Name, email=email, username=username,
                            password=password, contact_info=contact)
                user.save()
            if (choice == "trainer"):
                name = request.POST.get('Name', '')
                print(name)
                email = request.POST.get('email', '')
                print(email)
                username = request.POST.get('username', '')
                password = request.POST.get('Password', '')
                contact = request.POST.get('contact', '')
                trainer = Trainer(name=name, email=email, username=username,
                                  password=password, contact_info=contact)
                trainer.save()

    students = User.objects.all()
    trainers = Trainer.objects.all()
    print("this is the newwwwww USER", new)
    context = {
        'students': students,
        'trainers':  Trainer.objects.prefetch_related('trainerinfo_set').all(),
        'courses': Course.objects.all(),
    }
    return render(request, 'learning/index.html', context)


def about(request):
    return render(request, 'learning/about.html')


def courses(request):
    login_status = ""
    USR = ""
    if request.method == "POST":
        if "loginForm" in request.POST:
            # Process login form
            userID = request.POST.get("UserID", "")
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            userType = request.POST.get('userType', '')
            if userType == 'student':
                try:
                    student = User.objects.get(username=username)
                    if student.password == password:
                        USR = username
                        print(username, " has logged in as a user or student")
                        login_status = "success"
                    else:
                        print("wrong password by user")
                        login_status = "wrong_password"
                except User.DoesNotExist:
                    print("user not registered")
                    login_status = "not_registered"
            elif userType == 'trainer':
                try:
                    trainer = Trainer.objects.get(username=username)
                    if trainer.password == password:
                        USR = username
                        print(username, " has logged in as a trainer")
                        login_status = "success"
                    else:
                        print("wrong password by trainer")
                        login_status = "wrong_password"
                except Trainer.DoesNotExist:
                    print("this trainer doesn't exist")
                    login_status = "not_registered"

            # Return JSON response
            return JsonResponse({'login_status': login_status},)

        elif "signupForm" in request.POST:
            # Process signup form
            choice = request.POST.get('userType', '')
            print("the choice is: ", choice)
            if (choice == "student"):
                Name = request.POST.get('Name', '')
                print(Name)
                email = request.POST.get('email', '')
                print(email)
                username = request.POST.get('username', '')
                password = request.POST.get('Password', '')
                contact = request.POST.get('contact', '')
                print("user data saved")
                user = User(Name=Name, email=email, username=username,
                            password=password, contact_info=contact)
                user.save()
            if (choice == "trainer"):
                name = request.POST.get('Name', '')
                print(name)
                email = request.POST.get('email', '')
                print(email)
                username = request.POST.get('username', '')
                password = request.POST.get('Password', '')
                contact = request.POST.get('contact', '')
                trainer = Trainer(name=name, email=email, username=username,
                                  password=password, contact_info=contact)
                trainer.save()
    context = {
        'trainers':  Trainer.objects.prefetch_related('trainerinfo_set').all(),
        'courses': Course.objects.all(),
    }
    return render(request, 'learning/courses.html', context)


def create_course(request):
    trainers = Trainer.objects.all()
    if request.method == 'POST':
        trainer_id = request.POST.get('trainer_id')
        title = request.POST.get('title')
        course_type = request.POST.get('type')
        duration = request.POST.get('duration')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('image')

        # Retrieve the trainer with the provided trainer ID
        try:
            trainer = Trainer.objects.get(TrinerID=trainer_id)
        except Trainer.DoesNotExist:
            return redirect('create')

        # Create the course object
        course = Course(
            title=title,
            Type=course_type,
            Trinerid=trainer,
            duration=duration,
            description=description,
            price=price,
            image=image
        )
        course.save()

        return redirect('courses')

    return render(request, 'learning/create.html', {'trainers': trainers})


def course_detail(request, course_id):
    if request.method == 'POST':
        # Enrollment request handling
        if not request.user.is_authenticated:
            # User is not logged in, return an error response
            return JsonResponse({'enrollment_status': 'failure', 'message': 'User is not logged in.'})

        # Retrieve the course object
        course = get_object_or_404(Course, CourseID=course_id)

        return JsonResponse({'enrollment_status': 'success', 'message': 'Enrollment successful.'})
    else:
        # Rendering the course details page
        course = get_object_or_404(Course, CourseID=course_id)
        lessons = course.lesson_set.all()
        return render(request, 'learning/course-details.html', {'course': course, 'lessons': lessons})


def events(request):
    return render(request, 'learning/events.html')

def contact(request):
    if request.method == 'POST':
        userid=request.POST.get('userID', '')
        if request.user.is_authenticated:
            user = get_object_or_404(User, UserID=userid)
        
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')

        # Save the contact message to the database
        contact_message = ContactUs(UserID=user, Subject=subject, message=message)
        contact_message.save()

        # You can also send an email notification to the admin here

        return render(request, 'learning/contact.html', {'success': True})

    users = User.objects.all()
    return render(request, 'learning/contact.html', {'users': users})

def create(request):
    context = {
        'trainers': Trainer.objects.all(),
        'courses': Course.objects.all()
    }
    return render(request, 'learning/create.html', context)


def trainers(request):
    login_status = ""
    USR = ""
    if request.method == "POST":
        if "loginForm" in request.POST:
            # Process login form
            userID = request.POST.get("UserID", "")
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            userType = request.POST.get('userType', '')
            if userType == 'student':
                try:
                    student = User.objects.get(username=username)
                    if student.password == password:
                        USR = username
                        print(username, " has logged in as a user or student")
                        login_status = "success"
                    else:
                        print("wrong password by user")
                        login_status = "wrong_password"
                except User.DoesNotExist:
                    print("user not registered")
                    login_status = "not_registered"
            elif userType == 'trainer':
                try:
                    trainer = Trainer.objects.get(username=username)
                    if trainer.password == password:
                        USR = username
                        print(username, " has logged in as a trainer")
                        login_status = "success"
                    else:
                        print("wrong password by trainer")
                        login_status = "wrong_password"
                except Trainer.DoesNotExist:
                    print("this trainer doesn't exist")
                    login_status = "not_registered"

            # Return JSON response
            return JsonResponse({'login_status': login_status},)

        elif "signupForm" in request.POST:
            # Process signup form
            choice = request.POST.get('userType', '')
            print("the choice is: ", choice)
            if (choice == "student"):
                Name = request.POST.get('Name', '')
                print(Name)
                email = request.POST.get('email', '')
                print(email)
                username = request.POST.get('username', '')
                password = request.POST.get('Password', '')
                contact = request.POST.get('contact', '')
                print("user data saved")
                user = User(Name=Name, email=email, username=username,
                            password=password, contact_info=contact)
                user.save()
            if (choice == "trainer"):
                name = request.POST.get('Name', '')
                print(name)
                email = request.POST.get('email', '')
                print(email)
                username = request.POST.get('username', '')
                password = request.POST.get('Password', '')
                contact = request.POST.get('contact', '')
                trainer = Trainer(name=name, email=email, username=username,
                                  password=password, contact_info=contact)
                trainer.save()
    context = {
        'trainers':  Trainer.objects.prefetch_related('trainerinfo_set').all(),
        'user': USR,
    }
    return render(request, 'learning/trainers.html', context)


def course_detail(request, course_id):
    if request.method == 'POST':
        # Enrollment request handling
        if not request.user.is_authenticated:
            # User is not logged in, return an error response
            return JsonResponse({'enrollment_status': 'failure', 'message': 'User is not logged in.'})
        else:
            # Retrieve the course object
            course = get_object_or_404(Course, CourseID=course_id)

            # Perform the enrollment logic here
            # For example, you can create a new enrollment object and associate it with the user and the course

            # Return a success response
            return JsonResponse({'enrollment_status': 'success', 'message': 'Enrollment successful.'})
    else:
        # Rendering the course details page
        course = get_object_or_404(Course, CourseID=course_id)
        lessons = course.lesson_set.all()
        return render(request, 'learning/course-details.html', {'course': course, 'lessons': lessons})


def enroll(request, course_id):
    if request.method == 'POST':
        # Enrollment request handling
        if not request.user.is_authenticated:
            # User is not logged in, return an error response
            return JsonResponse({'enrollment_status': 'failure', 'message': 'User is not logged in.'})
        else:
            # Retrieve the course object
            course = get_object_or_404(Course, CourseID=course_id)
            if(course.price == 0):
                # Return a success response
                return JsonResponse({'enrollment_status': 'success', 'message': 'Enrollment successful.'})
            else:
                return JsonResponse({'enrollment_status': 'failure', 'message': 'course is not free.'})
    else:
        # Rendering the course details page
        course = get_object_or_404(Course, CourseID=course_id)
        lessons = course.lesson_set.all()

        return render(request, 'learning/enroll.html', {'course': course, 'lessons': lessons})

def pricing(request, course_id):
    course = get_object_or_404(Course, CourseID=course_id)
    return render(request, 'learning/pricing.html',{'course': course})

def add_lesson(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        duration = request.POST['duration']
        order = request.POST['order']
        resources = request.FILES['resources']
        courseId = request.POST['courseId']
        trainerId = request.POST['trainer_id']

        # Retrieve the Course object using the courseId
        course = get_object_or_404(Course, CourseID=courseId)

        # Retrieve the Trainer object using the trainerId
        trainer = get_object_or_404(Trainer, TrinerID=trainerId)

        # Check if the trainer is associated with the course
        if not course.Trinerid != trainerId:
            return render(request, 'learning/create.html', {'trainers': Trainer.objects.all(), 'courses': Course.objects.all(), 'error_message': 'Wrong trainer for this course'})

        # Create the Lesson instance with the retrieved Course and Trainer objects
        lesson = Lesson(title=title, content=content, duration=duration,
                        order=order, resources=resources, CourseID=course)

        # Save the lesson to the database
        lesson.save()

        # Perform any additional processing or redirection here
        # Redirect to the trainers page after successful submission
        return redirect('create')

    trainers = Trainer.objects.all()
    courses = Course.objects.all()

    return render(request, 'learning/create.html', {'trainers': trainers, 'courses': courses})


def trainer_details(request):
    trainers = Trainer.objects.all()  # Retrieve all trainers from the database

    if request.method == 'POST':
        trainer_id = request.POST.get('trainer_id')
        profession = request.POST.get('profession')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        # Retrieve the Trainer object based on the trainer_id
        # Convert the trainer_id to an integer
        trainer = get_object_or_404(Trainer, TrinerID=int(trainer_id))

        # Check if a Trainerinfo object already exists for the trainer
        trainer_info = Trainerinfo.objects.filter(Trinerid=trainer).first()

        if trainer_info:
            # Update the existing Trainerinfo object with the new details
            trainer_info.profession = profession
            trainer_info.description = description
            if image:
                trainer_info.image = image
            trainer_info.save()
        else:
            # Create a new Trainerinfo object and save it to the database
            trainer_info = Trainerinfo(
                Trinerid=trainer,
                profession=profession,
                description=description,
            )
            if image:
                trainer_info.image = image
            trainer_info.save()

        # Redirect to the trainers page after successful submission
        return redirect('trainers')

    return render(request, 'learning/trainers.html', {'trainers': trainers})
