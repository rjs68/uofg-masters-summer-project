from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from teach_app_backend.managers import TeachUserManager


class TeachUser(AbstractBaseUser):
    email = models.EmailField(primary_key=True, unique=True)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    profile_picture = models.ImageField(upload_to='profile_pictures')

    is_teacher = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    objects = TeachUserManager()

    def __str__(self):
        return self.email


class Unit(models.Model):
    unit_name = models.CharField(max_length=128)
    teacher = models.ForeignKey(TeachUser, on_delete=models.CASCADE)
    number_of_credits = models.IntegerField()

    class Meta:
        unique_together = ('unit_name', 'teacher')

    def __str__(self):
        return self.unit_name


class UserEnrolledClass(models.Model):
    user = models.ForeignKey(TeachUser, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'unit')

    def __str__(self):
        return self.user + "_" + self.unit


class Event(models.Model):
    event_name = models.CharField(max_length=128)
    date_time = models.DateTimeField()

    def __str__(self):
        return self.event_name


class Assignment(Event):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    specification = models.FileField(upload_to='assignments')
    weight = models.DecimalField(max_digits=3, decimal_places=2)

    def __str__(self):
        return self.event_name


class Submission(models.Model):
    user = models.ForeignKey(TeachUser, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    submission = models.FileField(upload_to='submissions')
    submission_time = models.DateTimeField()
    grade = models.DecimalField(max_digits=4, decimal_places=2)
    feedback = models.TextField()

    class Meta:
        unique_together = ('user', 'assignment')

    def __str__(self):
        return self.user + "_" + self.assignment


class Lecture(Event):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    lecture_name = models.CharField(max_length=128)
    link = models.CharField(max_length=128)

    def __str__(self):
        return self.lecture_name


class Quiz(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    total_mark = models.IntegerField()

    def __str__(self):
        return self.lecture + "_quiz"


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.TextField()

    def __str__(self):
        return "question_" + self.id


class Answer(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    answer = models.TextField()
    is_correct = models.BooleanField()

    def __str__(self):
        return self.answer


class UserAnswer(models.Model):
    user = models.ForeignKey(TeachUser, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'question')

    def __str__(self):
        return self.user + "_" + self.question


class UserQuizPerformance(models.Model):
    user = models.ForeignKey(TeachUser, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    grade = models.IntegerField()

    class Meta:
        unique_together = ('user', 'quiz')

    def __str__(self):
        return self.user + "_" + self.quiz
