from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from teach_app_backend.managers import TeachUserManager


class University(models.Model):
    university_name = models.CharField(primary_key=True, max_length=128, unique=True)
    teacher_enrol_key = models.CharField(max_length=16, unique=True)
    student_enrol_key = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.university_name


class TeachUser(AbstractBaseUser):
    email = models.EmailField(primary_key=True, unique=True)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures')

    is_teacher = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name', 'university']

    objects = TeachUserManager()

    def __str__(self):
        return self.email


class Unit(models.Model):
    unit_code = models.IntegerField(primary_key=True, unique=True)
    unit_name = models.CharField(max_length=128)
    teacher = models.ForeignKey(TeachUser, on_delete=models.CASCADE)
    unit_enrol_key = models.CharField(max_length=16)
    number_of_credits = models.IntegerField()

    class Meta:
        unique_together = ('unit_name', 'teacher')

    def __str__(self):
        return self.unit_name


class UserEnrolledUnit(models.Model):
    user = models.ForeignKey(TeachUser, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'unit')

    def __str__(self):
        return self.user.__str__() + "_" + self.unit.__str__()


class Event(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=128)
    date_time = models.DateTimeField()

    class Meta:
        unique_together = ('unit', 'event_name')

    def __str__(self):
        return self.unit + "_" + self.event_name


class Assignment(Event):
    specification = models.FileField(upload_to='assignments')
    weight = models.DecimalField(max_digits=3, decimal_places=2)

    def __str__(self):
        return self.unit.__str__() + "_" + self.event_name


class Submission(models.Model):
    user = models.ForeignKey(TeachUser, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    submission = models.FileField(upload_to='submissions')
    submission_time = models.DateTimeField(blank=True, null=True)
    grade = models.DecimalField(blank=True, null=True, default=None, max_digits=4, decimal_places=2)
    feedback = models.TextField(blank=True, null=True, default=None)

    class Meta:
        unique_together = ('user', 'assignment')

    def __str__(self):
        return self.user.__str__() + "_" + self.assignment.__str__()


class Lecture(Event):
    link = models.CharField(max_length=128)

    def __str__(self):
        return self.event_name


class Quiz(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    total_mark = models.IntegerField()

    def __str__(self):
        return "quiz_" + str(self.id)


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.TextField()

    def __str__(self):
        return "question_" + str(self.id)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
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
        return self.user.__str__() + "_" + self.answer.__str__()


class UserQuizPerformance(models.Model):
    user = models.ForeignKey(TeachUser, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    grade = models.IntegerField()

    class Meta:
        unique_together = ('user', 'quiz')

    def __str__(self):
        return self.user.__str__() + "_" + self.quiz.__str__()
