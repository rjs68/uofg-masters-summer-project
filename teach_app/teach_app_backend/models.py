from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.exceptions import ObjectDoesNotExist

from teach_app_backend.managers import TeachUserManager


class University(models.Model):
    university_name = models.CharField(primary_key=True, max_length=128, unique=True)
    teacher_enrol_key = models.CharField(max_length=16, unique=True)
    student_enrol_key = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.university_name


class TeachUser(AbstractBaseUser):
    #custom user model overwritting template provided by Django
    email = models.EmailField(primary_key=True, unique=True)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures')

    #sets default admin privileges
    is_teacher = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    #methods to determine user permissions
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    #set username field as email
    USERNAME_FIELD = 'email'

    #sets required fields, password included in base model
    REQUIRED_FIELDS = ['first_name', 'last_name', 'university']

    #points to manager which determines how users should be created
    objects = TeachUserManager()

    def __str__(self):
        return self.email


class Unit(models.Model):
    unit_code = models.IntegerField(primary_key=True, unique=True)
    unit_name = models.CharField(max_length=128)
    teacher = models.ForeignKey(TeachUser, on_delete=models.CASCADE)
    unit_enrol_key = models.CharField(max_length=16)
    number_of_credits = models.IntegerField()

    def save(self, *args, **kwargs):
        #overwritten save method to ensure unit_code is unique and 
        #number_of_credits is at least 1
        unit_code_unique = False
        while not unit_code_unique:
            try:
                unit = Unit.objects.get(unit_code=self.unit_code)
                self.unit_code += 1
            except ObjectDoesNotExist:
                unit_code_unique = True
        
        if self.number_of_credits<1:
            self.number_of_credits=1
        
        super(Unit, self).save(*args, **kwargs)

    class Meta:
        #ensure teacher cannot teach 2 units with the same name
        unique_together = ('unit_name', 'teacher')

    def __str__(self):
        return self.unit_name


class UserEnrolledUnit(models.Model):
    user = models.ForeignKey(TeachUser, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    class Meta:
        #sets primary key as combination of user and unit
        unique_together = ('user', 'unit')

    def __str__(self):
        return self.user.__str__() + "_" + self.unit.__str__()


class Event(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=128)
    date_time = models.DateTimeField()

    class Meta:
        #sets primary key as combination of unit and event_name
        unique_together = ('unit', 'event_name')

    def __str__(self):
        return self.unit.__str__() + "_" + self.event_name


class Assignment(Event):
    specification = models.FileField(upload_to='assignments')
    weight = models.DecimalField(max_digits=3, decimal_places=2)

    def save(self, *args, **kwargs):
        #overwritten save method ensuring assignment weight is between 0 and 1
        if isinstance(self.weight, str):
                self.weight = float(self.weight) 
        if self.weight<=0:
            self.weight=0.01
        elif self.weight>1:
            self.weight=1
        
        super(Assignment, self).save(*args, **kwargs)

    def __str__(self):
        return self.unit.__str__() + "_" + self.event_name


class Submission(models.Model):
    user = models.ForeignKey(TeachUser, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    #files upload to submissions folder in media
    submission = models.FileField(upload_to='submissions')
    submission_time = models.DateTimeField(blank=True, null=True)
    grade = models.DecimalField(blank=True, null=True, default=None, max_digits=5, decimal_places=2)
    feedback = models.TextField(blank=True, null=True, default=None)

    def save(self, *args, **kwargs):
        #overwritten save method to ensure grade is between 0 and 100
        if self.grade:
            if isinstance(self.grade, str):
                self.grade = float(self.grade) 
            if self.grade<0:
                self.grade=0.00
            elif self.grade>100:
                self.grade=100.00
        
        super(Submission, self).save(*args, **kwargs)

    class Meta:
        #sets primary key as a combination of user and assignment
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

    def save(self, *args, **kwargs):
        #overwritten save method to ensure total_mark is not negative
        if self.total_mark:
            if self.total_mark<0:
                self.total_mark=0
        else:
            self.total_mark = 0
        
        super(Quiz, self).save(*args, **kwargs)

    def __str__(self):
        return "quiz_" + str(self.id)


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.TextField()

    def save(self, *args, **kwargs):
        #overwritten save method updates the total_mark of the quiz
        previous_number_of_questions = Question.objects.filter(quiz=self.quiz).count()
        new_quiz_mark = previous_number_of_questions + 1
        self.quiz.total_mark = new_quiz_mark
        self.quiz.save()
        
        super(Question, self).save(*args, **kwargs)


    def __str__(self):
        return "question_" + str(self.id)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()
    is_correct = models.BooleanField()

    def save(self, *args, **kwargs):
        #overwritten save method ensures only one answer is correct
        if(self.is_correct==True):
            answers = Answer.objects.filter(question=self.question)
            for answer in answers:
                if answer.is_correct:
                    self.is_correct=False
        
        super(Answer, self).save(*args, **kwargs)

    def __str__(self):
        return self.answer


class UserAnswer(models.Model):
    user = models.ForeignKey(TeachUser, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        #overwritten save method ensures user only has one answer for a question
        try:
            user_answer = UserAnswer.objects.get(user=self.user, question=self.question).delete()
        except ObjectDoesNotExist:
            pass
        finally:
            super(UserAnswer, self).save(*args, **kwargs)

    class Meta:
        #sets primary key as combination between user and question
        unique_together = ('user', 'question')

    def __str__(self):
        return self.user.__str__() + "_" + self.answer.__str__()


class UserQuizPerformance(models.Model):
    user = models.ForeignKey(TeachUser, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    grade = models.IntegerField()

    def save(self, *args, **kwargs):
        #overwritten save method ensures grade is between 0 and the total quiz mark
        #and user only has one performance for a quiz
        if(self.grade>self.quiz.total_mark):
            self.grade=self.quiz.total_mark
        elif(self.grade<0):
            self.grade=0
        try:
            user_quiz_performance = UserQuizPerformance.objects.get(user=self.user, quiz=self.quiz).delete()
        except ObjectDoesNotExist:
            pass
        finally:
            super(UserQuizPerformance, self).save(*args, **kwargs)

    class Meta:
        #sets primary key as a combination of user and quiz
        unique_together = ('user', 'quiz')

    def __str__(self):
        return self.user.__str__() + "_" + self.quiz.__str__()
