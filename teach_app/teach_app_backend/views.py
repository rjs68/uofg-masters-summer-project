import simplejson as json
import os
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, FileResponse
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import generics
from datetime import datetime

from teach_app_backend.models import (TeachUser, University, Unit, UserEnrolledUnit, Assignment, Submission,
                                        Lecture, Quiz, Question, Answer, UserAnswer)
from teach_app_backend.serializers import TeachUserSerializer, UnitSerializer
from populate_teach import (add_user, add_unit, add_unit_enrolled, add_assignment, add_user_answer, 
                            add_user_quiz_performance)


@csrf_exempt
def get_user_units(request):
    data = json.loads(request.body)
    user = TeachUser.objects.get(email=data['email'])

    user_units = __get_user_units(user)
    units = []
    for user_unit in user_units:
            unit_data = __get_unit_data(user_unit)
            units.append(unit_data)
    
    units_data = json.dumps(units)
    return HttpResponse(units_data)


@csrf_exempt
def get_user_assignments(request):
    data = json.loads(request.body)
    user = TeachUser.objects.get(email=data['email'])

    user_units = __get_user_units(user)
    assignments = []
    for user_unit in user_units:
        unit_assignments = Assignment.objects.filter(unit=user_unit)
        for unit_assignment in unit_assignments:
            assignment_data = __get_assignment_data(unit_assignment)
            assignments.append(assignment_data)
    
    data = json.dumps(assignments, default=str)
    return HttpResponse(data)


@csrf_exempt
def get_user_lectures(request):
    data = json.loads(request.body)
    user = TeachUser.objects.get(email=data['email'])

    user_units = __get_user_units(user)
    lectures = []
    for user_unit in user_units:
        unit_lectures = Lecture.objects.filter(unit=user_unit)
        for unit_lecture in unit_lectures:
            lecture_data = __get_lecture_data(unit_lecture)
            lectures.append(lecture_data)
    
    data = json.dumps(lectures, default=str)
    return HttpResponse(data)


@csrf_exempt
def get_assignment_specification(request):
    data = json.loads(request.body)
    unit = Unit.objects.get(unit_code=data['unitCode'])
    assignment = Assignment.objects.get(unit=unit, event_name=data['assignmentName'])
    if(assignment.specification):
        return HttpResponse("Specification found")
    else:
        return HttpResponse("Specification not found")


@csrf_exempt
def upload_assignment_specification(request):
    specification = request.FILES['specification']
    specification_name = specification.name.split('-')
    unit = Unit.objects.get(unit_code=specification_name[1])
    assignment_name = specification_name[2].split('.')
    assignment = Assignment.objects.get(unit=unit, event_name=assignment_name[0])
    assignment.specification = specification
    assignment.save()
    if(assignment.specification):
        return HttpResponse("Upload Successful")
    else:
        return HttpResponse("Upload Unsuccessful")


@csrf_exempt
def get_submission(request):
    data = json.loads(request.body)
    user = TeachUser.objects.get(email=data['userEmail'])
    unit = Unit.objects.get(unit_code=data['unitCode'])
    assignment = Assignment.objects.get(unit=unit, event_name=data['assignmentName'])
    submission = __get_submission_object(user, assignment)
    if(submission.submission):
        submission_data = __get_submission_data(submission)
        submission_data = json.dumps(submission_data, default=str)
        return HttpResponse(submission_data)
    else:
        return HttpResponse("Submission not found")


@csrf_exempt
def get_student_submissions(request):
    data = json.loads(request.body)
    unit = Unit.objects.get(unit_code=data['unitCode'])
    assignment = Assignment.objects.get(unit=unit, event_name=data['assignmentName'])
    submissions = Submission.objects.filter(assignment=assignment)
    submissions_data = []
    if(submissions):
        for submission in submissions:
            submission_data = __get_submission_data(submission)
            submissions_data.append(submission_data)
        
        submissions_data = json.dumps(submissions_data, default=str)
        return HttpResponse(submissions_data)
    else:
        return HttpResponse("No submissions yet")


@csrf_exempt
def edit_student_grade(request):
    data = json.loads(request.body)
    user = TeachUser.objects.get(email=data['studentEmail'])
    unit = Unit.objects.get(unit_code=data['unitCode'])
    assignment = Assignment.objects.get(unit=unit, event_name=data['assignmentName'])
    submission = __get_submission_object(user, assignment)

    submission.grade = data['grade']
    submission.save()
    if(submission.grade == data['grade']):
        return HttpResponse("Grade Edit Successful")
    else:
        return HttpResponse("Grade Edit Unsuccessful")


@csrf_exempt
def edit_student_feedback(request):
    data = json.loads(request.body)
    user = TeachUser.objects.get(email=data['studentEmail'])
    unit = Unit.objects.get(unit_code=data['unitCode'])
    assignment = Assignment.objects.get(unit=unit, event_name=data['assignmentName'])
    submission = __get_submission_object(user, assignment)

    submission.feedback = data['feedback']
    submission.save()
    if(submission.feedback == data['feedback']):
        return HttpResponse("Feedback Edit Successful")
    else:
        return HttpResponse("Feedback Edit Unsuccessful")


@csrf_exempt
def upload_submission(request):
    submission_file = request.FILES['submission']
    submission_name = submission_file.name.split('-')
    assignment_name = submission_name[2].split('.')

    user = TeachUser.objects.get(email=submission_name[0])
    unit = Unit.objects.get(unit_code=submission_name[1])
    assignment = Assignment.objects.get(unit=unit, event_name=assignment_name[0])
    submission = Submission.objects.get(user=user, assignment=assignment)

    directory_name = os.path.join(settings.MEDIA_ROOT, "submissions")
    file_name = submission_file.name.replace('@', '')
    file_path = os.path.join(directory_name, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)
    submission.submission = submission_file
    submission.submission_time = datetime.now()
    submission.save()

    if(submission.submission):
        return HttpResponse("Upload Successful")
    else:
        return HttpResponse("Upload Unsuccessful")


@csrf_exempt
def create_unit(request):
    data = json.loads(request.body)
    unit_code = data['unitCode']
    unit_name = data['unitName']
    teacher = data['teacher']
    unit_enrol_key = data['unitEnrolmentKey']
    number_of_credits = data['numberOfCredits']

    unit = add_unit(unit_code, unit_name, teacher, unit_enrol_key, number_of_credits)

    if unit:
        return HttpResponse("Unit Created Successfully")
    else:
        return HttpResponse("Unit Not Created")


@csrf_exempt
def create_assignment(request):
    data = json.loads(request.body)
    unit_code = data['unitCode']
    assignment_name = data['assignmentName']
    deadline_string = data['deadline']
    deadline = datetime.strptime(deadline_string, "%Y-%m-%dT%H:%M")
    weight = data['weight']

    assignment = add_assignment(unit_code, assignment_name, deadline, weight)

    if(assignment):
        return HttpResponse("Assignment Created Successfully")
    else:
        return HttpResponse("Assignment Not Created")


@csrf_exempt
def unit_enrolment(request):
    data = json.loads(request.body)
    unit_enrol_key = data['unitEnrolmentKey']
    email = data['email']
    unit = Unit.objects.get(unit_code=data['unitCode'])

    if unit and unit_enrol_key == unit.unit_enrol_key:
        user_enrolled_unit = add_unit_enrolled(email, unit_code)
        if(user_enrolled_unit):
            return HttpResponse("User Enrolled")
    else:
        return HttpResponse("User Not Enrolled")


@csrf_exempt
def authenticate_user(request):
    csrf_token = get_token(request)
    return HttpResponse(csrf_token)


# @csrf_exempt
def user_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # Retrieves username and password
        email = data['email']
        password = data['password']
        # Authenticates the user
        user = authenticate(request, email=email, password=password)

        if user:
            login(request, user)
            if user.is_teacher:
                return HttpResponse("Teacher Login Successful")
            else:
                return HttpResponse("Student Login Successful")
        else:
            # If there are any authentication errors, send error feedback
            return HttpResponse("Login Unsuccessful", status=401)
    else:
        return HttpResponse("Not a valid request")


@csrf_exempt
def user_signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        enrol_key = data['enrolmentKey']

        university = None
        is_teacher = None
        try:
            university = University.objects.get(teacher_enrol_key=enrol_key)
            is_teacher = True
        except:
            try:
                university = University.objects.get(student_enrol_key=enrol_key)
                is_teacher = False
            except:
                return HttpResponse("Invalid Enrolment Key", status=401)
        
        email = data['email']
        password = data['password']
        first_name = data['firstName']
        last_name = data['lastName']
        university_name = university.university_name

        user = add_user(email, password, first_name, last_name, university_name, is_teacher)

        if user:
            login(request, user)
            if is_teacher:
                return HttpResponse("Teacher Creation Successful")
            else:
                return HttpResponse("Student Creation Successful")
        else:
            # If there are any authentication errors, send error feedback
            return HttpResponse("User Creation Unsuccessful", status=401)
    else:
        return HttpResponse("Not a valid request")


@csrf_exempt
def get_quiz(request):
    data = json.loads(request.body)
    unit = Unit.objects.get(unit_code=data['unitCode'])
    lecture = Lecture.objects.get(unit=unit,
                                    event_name=data['lectureName'])
    quiz = Quiz.objects.filter(lecture=lecture)[0]
    if(quiz):
        quiz_data = {}
        questions = Question.objects.filter(quiz=quiz)
        for question in questions:
            answer_data = __get_answers(question)
            quiz_data[question.question] = answer_data
        quiz_data = json.dumps(quiz_data)
        return HttpResponse(quiz_data)
    else:
        return HttpRespons("No quiz available")


@csrf_exempt
def submit_user_answer(request):
    data=json.loads(request.body)

    unit_code=data['unitCode']
    event_name=data['lectureName']
    question=data['question']
    answer=data['answer']
    user_email=data['userEmail']

    unit = Unit.objects.get(unit_code=unit_code)
    lecture = Lecture.objects.get(unit=unit,
                                    event_name=event_name)
    quiz = Quiz.objects.filter(lecture=lecture)[0]
    question_object = Question.objects.get(quiz=quiz,
                                    question=question)

    question_answers = Answer.objects.filter(question=question_object)
    for question_answer in question_answers:
        try:
            userAnswer = UserAnswer.objects.get(user_email=user_email,
                                                answer=question_answer).delete()
        except:
            pass
    
    user_answer = add_user_answer(unit_code, event_name, question, answer, user_email)
    if(user_answer):
        return HttpResponse("Answer Submitted")
    else:
        return HttpResponse("Submission Error")


@csrf_exempt
def get_quiz_results(request):
    data = json.loads(request.body)

    unit_code=data['unitCode']
    event_name=data['lectureName']

    unit = Unit.objects.get(unit_code=unit_code)
    lecture = Lecture.objects.get(unit=unit,
                                    event_name=event_name)
    quiz = Quiz.objects.filter(lecture=lecture)[0]

    users = UserEnrolledUnit.objects.filter(unit=unit)
    user_performances = {}
    for user in users:
        user_email = user.user.email
        user_performance = add_user_quiz_performance(unit_code, event_name, user_email)
        user_performances[user_email] = user_performance.grade
    
    user_performances = json.dumps(user_performances)
    return HttpResponse(user_performances)


def __get_user_units(user):
    if user.is_teacher:
        user_units = Unit.objects.filter(teacher=user)
    else:
        user_enrolled_units = UserEnrolledUnit.objects.filter(user=user).values('unit')
        user_units = []
        for user_enrolled_unit in user_enrolled_units:
            unit = Unit.objects.get(unit_code=user_enrolled_unit['unit'])
            user_units.append(unit)
    return user_units


def __get_answers(question):
    answer_data = {}
    answers = Answer.objects.filter(question=question)
    for answer in answers:
        answer_data[answer.answer] = answer.is_correct
    return answer_data


def __get_unit_data(unit):
    return {
        "unit_code": unit.unit_code,
        "unit_name": unit.unit_name,
        "teacher": unit.teacher.email,
        "unit_enrol_key": unit.unit_enrol_key,
        "number_of_credits": unit.number_of_credits
    }


def __get_assignment_data(assignment):
    return {
        "unit": assignment.unit.unit_name,
        "unit_code": assignment.unit.unit_code,
        "assignment_name": assignment.event_name,
        "deadline": assignment.date_time.strftime("%Y-%m-%dT%H:%M:%S"),
        "weight": assignment.weight
    }


def __get_lecture_data(lecture):
    return {
        "unit": lecture.unit.unit_name,
        "unit_code": lecture.unit.unit_code,
        "lecture_name": lecture.event_name,
        "lecture_time": lecture.date_time.strftime("%Y-%m-%dT%H:%M:%S"),
    }


def __get_submission_data(submission):
    if(submission.submission_time):
        submission_time = submission.submission_time.strftime("%Y-%m-%dT%H:%M:%S")
    else:
        submission_time = None
    
    return {
        "user": submission.user.email,
        "submission_time": submission_time,
        "grade": submission.grade,
        "feedback": submission.feedback
    }


def __get_submission_object(user, assignment):
    try:
        submission = Submission.objects.get(user=user, assignment=assignment)
    except ObjectDoesNotExist:
        submission = Submission.objects.create(user=user, assignment=assignment)
    return submission
