import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework import generics

from teach_app_backend.models import TeachUser, University, Unit, UserEnrolledUnit, Assignment
from teach_app_backend.serializers import TeachUserSerializer, UnitSerializer
from populate_teach import add_user, add_unit, add_unit_enrolled


def index(request):
    return HttpResponse("Welcome to Teach")


class TeachUserListCreate(generics.ListCreateAPIView):
    queryset = TeachUser.objects.all()
    serializer_class = TeachUserSerializer


def get_user_units(request):
    data = json.loads(request.body)
    email = data['email']
    user = TeachUser.objects.get(email=email)
    units = []
    
    if user.is_teacher:
        user_units = Unit.objects.filter(teacher=user)
        for user_unit in user_units:
            unit_data = __get_unit_data(user_unit)
            units.append(unit_data)
    else:
        user_units = UserEnrolledUnit.objects.filter(user=user).values('unit')
        for user_unit in user_units:
            unit = Unit.objects.get(unit_code=user_unit['unit'])
            unit_data = __get_unit_data(unit)
            units.append(unit_data)
    
    data = json.dumps(units)
    return HttpResponse(data)


def get_user_assignments(request):
    data = json.loads(request.body)
    email = data['email']
    user = TeachUser.objects.get(email=email)

    assignments = []
    if user.is_teacher:
        user_units = Unit.objects.filter(teacher=user)
    else:
        user_enrolled_units = UserEnrolledUnit.objects.filter(user=user).values('unit')
        user_units = []
        for user_enrolled_unit in user_enrolled_units:
            unit = Unit.objects.get(unit_code=user_enrolled_unit['unit'])
            user_units.append(unit)
    for user_unit in user_units:
        unit_assignments = Assignment.objects.filter(unit=user_unit)
        for unit_assignment in unit_assignments:
            assignment_data = __get_assignment_data(unit_assignment)
            assignments.append(assignment_data)
    
    data = json.dumps(assignments, default=str)
    return HttpResponse(data)


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


def unit_enrolment(request):
    data = json.loads(request.body)
    unit_code = data['unitCode']
    unit_enrol_key = data['unitEnrolmentKey']
    email = data['email']

    unit = Unit.objects.get(unit_code=unit_code)

    if unit and unit_enrol_key == unit.unit_enrol_key:
        user_enrolled_unit = add_unit_enrolled(email, unit_code)
        if(user_enrolled_unit):
            return HttpResponse("User Enrolled")
    else:
        return HttpResponse("User Not Enrolled")



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
        "assignment_name": assignment.event_name,
        "deadline": assignment.date_time,
        "weight": assignment.weight
    }
