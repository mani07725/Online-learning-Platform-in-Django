from django.db import models
from django.contrib.auth.models import AbstractUser

# User Model: Represents a user of the e-learning platform.
class User(models.Model):
    UserID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=20)  # User's name
    email = models.EmailField()  # User's email address
    username = models.CharField(max_length=100)  # User's username
    password = models.CharField(max_length=100)  # User's password
    contact_info = models.CharField(max_length=100)  # User's contact information
    def __str__(self):
        return self.username
# Trainer Model: Represents a trainer on the e-learning platform.
class Trainer(models.Model):
    TrinerID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)  # Trainer's name
    email = models.EmailField()  # Trainer's email address
    username = models.CharField(max_length=100)  # Trainer's username
    password = models.CharField(max_length=100)  # Trainer's password
    contact_info = models.CharField(max_length=100)  # Trainer's contact information
    def __str__(self):
        return str(self.username)

class Trainerinfo(models.Model):
    Trinerid = models.ForeignKey(Trainer, to_field='TrinerID', on_delete=models.CASCADE)
    profession = models.CharField(max_length=100)
    description = models.TextField(null=True, default=None)
    image = models.ImageField(upload_to='trainer/images', default=None, null=True)
    def __str__(self):
        return self.profession
# Course Model: Represents a course offered on the e-learning platform.
class Course(models.Model):
    CourseID = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)  # Course title
    Type = models.CharField(max_length=100, null=True, default=None)  # Course type
    Trinerid = models.ForeignKey(Trainer, to_field='TrinerID', on_delete=models.CASCADE)  # Trainer associated with the course
    duration = models.IntegerField()  # Duration of the course
    description = models.TextField(null=True, default=None)
    price = models.DecimalField(max_digits=8, decimal_places=2)  # Price of the course
    Enrollment=models.IntegerField(null=True, default=None)
    image = models.ImageField(upload_to='course/images', default="", null=True)
    def __str__(self):
        return self.title
# Assignment Model: Represents an assignment for a specific course.
class Assignment(models.Model):
    AssignmentID = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)  # Assignment title
    description = models.TextField()  # Assignment description
    deadline = models.DateTimeField()  # Assignment deadline
    CourseID = models.ForeignKey(Course, to_field='CourseID', on_delete=models.CASCADE)  # Course associated with the assignment

# Lesson Model: Represents a lesson within a course.
class Lesson(models.Model):
    LessonID = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)  # Lesson title
    content = models.TextField()  # Lesson content
    duration = models.IntegerField()  # Duration of the lesson
    order = models.IntegerField()  # Order of the lesson within the course
    resources = models.FileField(upload_to='lesson_resources/files', default="", null=True)  # File resources for additional lesson resources
    CourseID = models.ForeignKey(Course, to_field='CourseID', on_delete=models.CASCADE)  # Course associated with the lesson
    def __str__(self):
        return self.title
# Enrollment Model: Represents a user's enrollment in a course.
class Enrollment(models.Model):
    EnrollmentID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)  # User enrolled in the course
    CourseID = models.ForeignKey(Course, on_delete=models.CASCADE)  # Course being enrolled in
    enrollment_date = models.DateTimeField(auto_now_add=True)  # Date and time of enrollment
    completion_status = models.BooleanField(default=False)  # Completion status of the course
    grade = models.CharField(max_length=10)  # Grade achieved in the course

    def __str__(self):
        return str(self.enrollment_date)
# DiscussionForum Model: Represents a discussion forum for a specific course.
class DiscussionForum(models.Model):
    FormID = models.AutoField(primary_key=True)
    topic = models.CharField(max_length=100)  # Discussion topic
    description = models.TextField()  # Discussion description
    CourseID = models.ForeignKey(Course, to_field='CourseID', on_delete=models.CASCADE)  # Course associated with the discussion forum
    UserID = models.ForeignKey(User, to_field='UserID', on_delete=models.CASCADE)  # User who initiated the discussion

# Payment Model: Represents a payment made by a user for a course.
class Payment(models.Model):
    UserID = models.ForeignKey(User, to_field='UserID', on_delete=models.CASCADE)  # User making the payment
    CourseID = models.ForeignKey(Course, to_field='CourseID', on_delete=models.CASCADE)  # Course for which the payment is made
    payment_date = models.DateTimeField(auto_now_add=True)  # Date and time of payment
    amount = models.DecimalField(max_digits=8, decimal_places=2)  # Payment amount
    payment_method = models.CharField(max_length=50)  # Payment method used

# Notification Model: Represents a notification for a user.
class Notification(models.Model):
    NotificationID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(User, to_field='UserID', on_delete=models.CASCADE)  # User receiving the notification
    message = models.TextField()  # Notification message
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp of the notification

# ContactUs Model: Represents a user's contact message sent to another user.
class ContactUs(models.Model):
    ContactID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(User, to_field='UserID', on_delete=models.CASCADE)  # User sending the contact message
    Subject = models.CharField(max_length=50,default="")
    message = models.TextField()  # Contact message content
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp of the contact message
    def __str__(self):
        return str(self.Subject)