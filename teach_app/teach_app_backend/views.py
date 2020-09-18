import simplejson as json
import os
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from datetime import datetime
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.timezone import make_aware

from teach_app_backend.models import (TeachUser, University, Unit, UserEnrolledUnit, Assignment, Submission,
                                        Lecture, Quiz, Question, Answer, UserAnswer)
#make use of methods from population script to add data to the database
from populate_teach import (add_user, add_unit, add_unit_enrolled, add_assignment, add_user_answer, 
                            add_user_quiz_performance, add_lecture, add_quiz)

'''
Login and Sign up Functionality
'''

@ensure_csrf_cookie
def user_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        #retrieves username and password
        email = data['email']
        password = data['password']
        #authenticates the user
        user = authenticate(request, email=email, password=password)

        if user:
            #logs the user in
            login(request, user)
            if user.is_teacher:
                return HttpResponse("Teacher Login Successful")
            else:
                return HttpResponse("Student Login Successful")
        else:
            #if there are any authentication errors, send error feedback
            return HttpResponse("Login Unsuccessful", status=401)
    else:
        return HttpResponse("Not a valid request", status=400)


def user_signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        #retrieves the university enrolment key
        enrol_key = data['enrolmentKey']

        university = None
        is_teacher = None
        #first tries to enrol as a teacher then tries as a student
        try:
            university = University.objects.get(teacher_enrol_key=enrol_key)
            is_teacher = True
        except:
            try:
                university = University.objects.get(student_enrol_key=enrol_key)
                is_teacher = False
            except:
                return HttpResponse("Invalid Enrolment Key", status=401)
        
        #retrieves the data about the user
        email = data['email']
        password = data['password']
        first_name = data['firstName']
        last_name = data['lastName']
        university_name = university.university_name

        #creates a new user in the database
        user = add_user(email, password, first_name, last_name, university_name, is_teacher)

        if user:
            login(request, user)
            if is_teacher:
                return HttpResponse("Teacher Creation Successful")
            else:
                return HttpResponse("Student Creation Successful")
        else:
            #if there are any errors, send error feedback
            return HttpResponse("User Creation Unsuccessful", status=401)
    else:
        return HttpResponse("Not a valid request", status=400)




'''
Unit Functionality
'''

def get_user_units(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        #retrieves email of user in questions
        user = TeachUser.objects.get(email=data['email'])

        user_units = __get_user_units(user)
        units = []
        for user_unit in user_units:
                unit_data = __get_unit_data(user_unit)
                units.append(unit_data)
        
        #turns unit data object into json
        units_data = json.dumps(units)
        return HttpResponse(units_data)
    else:
        return HttpResponse("Not a valid request", status=400)

def create_unit(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        #retrieves data about the new unit
        unit_code = data['unitCode']
        unit_name = data['unitName']
        teacher = data['teacher']
        unit_enrol_key = data['unitEnrolmentKey']
        number_of_credits = data['numberOfCredits']

        #creates a new unit in the database
        unit = add_unit(unit_code, unit_name, teacher, unit_enrol_key, number_of_credits)

        if unit:
            return HttpResponse("Unit Created Successfully")
        else:
            return HttpResponse("Unit Not Created")
    else:
        return HttpResponse("Not a valid request", status=400)


def unit_enrolment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        #retrieve data about the unit and user
        unit_enrol_key = data['unitEnrolmentKey']
        email = data['email']
        unit_code = data['unitCode']
        unit = Unit.objects.get(unit_code=unit_code)

        #ensure unit exists the enrolment key is correct
        if unit and unit_enrol_key == unit.unit_enrol_key:
            #creates new user enrolled unit object in the database
            user_enrolled_unit = add_unit_enrolled(email, unit_code)
            if(user_enrolled_unit):
                return HttpResponse("User Enrolled")
        else:
            #if unit doesn't exist or enrolment key is incorrect
            return HttpResponse("User Not Enrolled")
    else:
        return HttpResponse("Not a valid request", status=400)




'''
Lecture Functionality
'''

def get_user_lectures(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        #retrieve email address of the user
        user = TeachUser.objects.get(email=data['email'])

        user_units = __get_user_units(user)
        lectures = []
        for user_unit in user_units:
            unit_lectures = Lecture.objects.filter(unit=user_unit)
            for unit_lecture in unit_lectures:
                lecture_data = __get_lecture_data(unit_lecture)
                lectures.append(lecture_data)
        
        #convert lecture data into json
        data = json.dumps(lectures, default=str)
        return HttpResponse(data)
    else:
        return HttpResponse("Not a valid request", status=400)


def get_next_lecture(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        #retrieve email address of the user
        user = TeachUser.objects.get(email=data['email'])

        user_units = __get_user_units(user)
        next_lecture = None
        for user_unit in user_units:
            #only retrieves lectures that have not finished and sort them by date and time
            unit_lectures = Lecture.objects.filter(unit=user_unit).exclude(date_time__lt=datetime.now()).order_by('date_time')
            #retrieve first lecture in the list
            next_unit_lecture = unit_lectures.first()
            if next_lecture:
                #compare next_lecture to next_unit_lecture to see which starts first
                if next_unit_lecture.date_time < next_lecture.date_time:
                    next_lecture = next_unit_lecture
            else:
                next_lecture = next_unit_lecture
        
        if next_lecture:
            next_lecture_data = __get_lecture_data(next_lecture)
            #convert lecture data to json
            data = json.dumps(next_lecture_data)
            return HttpResponse(data)
        else:
            #user has no upcoming lectures
            return HttpResponse("No lecture available")
    else:
        return HttpResponse("Not a valid request", status=400)
            

def create_lecture(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        #retrieve data for new lecture
        unit_code = data['unitCode']
        event_name = data['lectureName']
        time_string = data['time']
        #create datetime object from provided lecture time
        time = make_aware(datetime.strptime(time_string, "%Y-%m-%dT%H:%M"))

        #create new lecture object in the database
        lecture = add_lecture(unit_code, event_name, time, "")

        if(lecture):
            return HttpResponse("Lecture Created Successfully")
        else:
            return HttpResponse("Lecture Not Created")
    else:
        return HttpResponse("Not a valid request", status=400)




'''
Assignment Functionality
'''

def get_user_assignments(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        #retrieve email of user in question
        user = TeachUser.objects.get(email=data['email'])

        user_units = __get_user_units(user)
        assignments = []
        for user_unit in user_units:
            unit_assignments = Assignment.objects.filter(unit=user_unit)
            for unit_assignment in unit_assignments:
                assignment_data = __get_assignment_data(unit_assignment)
                assignments.append(assignment_data)
        
        #convert assignment data to json
        data = json.dumps(assignments, default=str)
        return HttpResponse(data)
    else:
        return HttpResponse("Not a valid request", status=400)


def get_next_assignment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        #retrieve email address of user
        user = TeachUser.objects.get(email=data['email'])

        user_units = __get_user_units(user)
        next_assignment = None
        for user_unit in user_units:
            #only retrieves assignments with future deadlines sorted by deadline date and time
            unit_assignments = Assignment.objects.filter(unit=user_unit).exclude(date_time__lt=datetime.now()).order_by('date_time')
            #get the first assignment from the list
            next_unit_assignment = unit_assignments.first()
            if next_assignment and next_unit_assignment:
                #compare next assignment to next unit assignment to see which has a sooner deadline
                if next_unit_assignment.date_time < next_assignment.date_time:
                    next_assignment = next_unit_assignment
            elif next_unit_assignment:
                next_assignment = next_unit_assignment
        
        if next_assignment:
            next_assignment_data = __get_assignment_data(next_assignment)
            #convert assignment data to json
            data = json.dumps(next_assignment_data)
            return HttpResponse(data)
        else:
            #user has no upcoming assignments
            return HttpResponse("No assignment available")
    else:
        return HttpResponse("Not a valid request", status=400)
        

def create_assignment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        #retrieve data for new assignment
        unit_code = data['unitCode']
        assignment_name = data['assignmentName']
        deadline_string = data['deadline']
        #convert deadline to datetime object
        deadline = make_aware(datetime.strptime(deadline_string, "%Y-%m-%dT%H:%M"))
        weight = data['weight']

        #create new assignment object in database
        assignment = add_assignment(unit_code, assignment_name, deadline, weight)

        if(assignment):
            return HttpResponse("Assignment Created Successfully")
        else:
            return HttpResponse("Assignment Not Created")
    else:
        return HttpResponse("Not a valid request", status=400)


def get_assignment_specification(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        #retrieve data identifying assignment
        unit = Unit.objects.get(unit_code=data['unitCode'])
        assignment = Assignment.objects.get(unit=unit, event_name=data['assignmentName'])
        if(assignment.specification):
            return HttpResponse("Specification found")
        else:
            #assignment specification hasn't been uploaded
            return HttpResponse("Specification not found")
    else:
        return HttpResponse("Not a valid request", status=400)


def get_assignment_specification_name(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        #retrieve data identifying assignment
        unit = Unit.objects.get(unit_code=data['unitCode'])
        assignment = Assignment.objects.get(unit=unit, event_name=data['assignmentName'])

        #retrieve full path for specification
        specification_path = assignment.specification.name
        specification_path_array = specification_path.split('/')

        #retrieves the name of the specification from the path
        specification_name = specification_path_array[-1]

        #converts specification name to json
        specification_name = json.dumps(specification_name)
        return HttpResponse(specification_name)
    else:
        return HttpResponse("Not a valid request", status=400)


def upload_assignment_specification(request):
    if request.method == 'POST':
        #retrieves specification file
        specification = request.FILES['specification']

        #determines unit and assignment from specification filename
        specification_name = specification.name.split('-')
        unit = Unit.objects.get(unit_code=specification_name[1])
        assignment_name = specification_name[2].split('.')
        assignment = Assignment.objects.get(unit=unit, event_name=assignment_name[0])

        #determine the file path for the assignment specification
        directory_name = os.path.join(settings.MEDIA_ROOT, "assignments")
        file_path = os.path.join(directory_name, specification.name)
        if os.path.exists(file_path):
            #if a specification already exists it's deleted
            os.remove(file_path)

        #new assignment specification saved
        assignment.specification = specification
        assignment.save()

        if(assignment.specification):
            return HttpResponse("Upload Successful")
        else:
            return HttpResponse("Upload Unsuccessful")
    else:
        return HttpResponse("Not a valid request", status=400)


def get_submission(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        #retrieves data about user and assignment
        user = TeachUser.objects.get(email=data['userEmail'])
        unit = Unit.objects.get(unit_code=data['unitCode'])
        assignment = Assignment.objects.get(unit=unit, event_name=data['assignmentName'])
        submission = __get_submission_object(user, assignment)
        if(submission.submission):
            submission_data = __get_submission_data(submission)
            #convert submission data to json
            submission_data = json.dumps(submission_data, default=str)
            return HttpResponse(submission_data)
        else:
            #no submission found for the user
            return HttpResponse("Submission not found")
    else:
        return HttpResponse("Not a valid request", status=400)


def get_submission_name(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        #retrieves data about the user and assignment
        user = TeachUser.objects.get(email=data['userEmail'])
        unit = Unit.objects.get(unit_code=data['unitCode'])
        assignment = Assignment.objects.get(unit=unit, event_name=data['assignmentName'])
        submission = __get_submission_object(user, assignment)

        #retrieves the full path of the submission file
        submission_path = submission.submission.name
        submission_path_array = submission_path.split('/')

        #retrieves the submission name from the file path
        submission_name = submission_path_array[-1]

        #converts the submission name to json
        submission_name = json.dumps(submission_name)
        return HttpResponse(submission_name)
    else:
        return HttpResponse("Not a valid request", status=400)


def upload_submission(request):
    if request.method == 'POST':
        #retrieves the submission file
        submission_file = request.FILES['submission']
        submission_name = submission_file.name.split('-')
        assignment_name = submission_name[2].split('.')

        #determines the user, unit, assignment and submission from the file name
        user = TeachUser.objects.get(email=submission_name[0])
        unit = Unit.objects.get(unit_code=submission_name[1])
        assignment = Assignment.objects.get(unit=unit, event_name=assignment_name[0])
        submission = Submission.objects.get(user=user, assignment=assignment)

        directory_name = os.path.join(settings.MEDIA_ROOT, "submissions")
        #removes '@' characters which can't be used in file names
        file_name = submission_file.name.replace('@', '')
        #determines file path of the submission
        file_path = os.path.join(directory_name, file_name)
        if os.path.exists(file_path):
            #if a submission already exists it is removed
            os.remove(file_path)

        #new submission is saved and the submission time is set to the time now
        submission.submission = submission_file
        submission.submission_time = make_aware(datetime.now())
        submission.save()

        if(submission.submission):
            return HttpResponse("Upload Successful")
        else:
            return HttpResponse("Upload Unsuccessful")
    else:
        return HttpResponse("Not a valid request", status=400)


def get_student_submissions(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        #retrieve data to identify the assignment
        unit = Unit.objects.get(unit_code=data['unitCode'])
        assignment = Assignment.objects.get(unit=unit, event_name=data['assignmentName'])

        #obtains all submissions for the assignment
        submissions = Submission.objects.filter(assignment=assignment)
        submissions_data = []
        if submissions:
            for submission in submissions:
                submission_data = __get_submission_data(submission)
                submissions_data.append(submission_data)
            
            #convert submission data to json
            submissions_data = json.dumps(submissions_data, default=str)
            return HttpResponse(submissions_data)
        else:
            #no students have submitted the assignment yet
            return HttpResponse("No submissions yet")
    else:
        return HttpResponse("Not a valid request", status=400)


def edit_student_grade(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        #retrieve data about the student and assignment
        user = TeachUser.objects.get(email=data['studentEmail'])
        unit = Unit.objects.get(unit_code=data['unitCode'])
        assignment = Assignment.objects.get(unit=unit, event_name=data['assignmentName'])
        submission = __get_submission_object(user, assignment)

        #update the grade for the submission
        submission.grade = data['grade']
        submission.save()
        if(submission.grade == float(data['grade'])):
            #ensure new grade matches the provided grade
            return HttpResponse("Grade Edit Successful")
        else:
            return HttpResponse("Grade Edit Unsuccessful")
    else:
        return HttpResponse("Not a valid request", status=400)


def edit_student_feedback(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        #retrieve data about the student and assignment
        user = TeachUser.objects.get(email=data['studentEmail'])
        unit = Unit.objects.get(unit_code=data['unitCode'])
        assignment = Assignment.objects.get(unit=unit, event_name=data['assignmentName'])
        submission = __get_submission_object(user, assignment)

        #update the feedback for the submission
        submission.feedback = data['feedback']
        submission.save()
        if(submission.feedback == data['feedback']):
            #ensure feedback matches the provided feedback
            return HttpResponse("Feedback Edit Successful")
        else:
            return HttpResponse("Feedback Edit Unsuccessful")
    else:
        return HttpResponse("Not a valid request", status=400)




'''
Quiz Functionality
'''

def get_quiz(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        #retrieves data about the unit and lecture
        unit = Unit.objects.get(unit_code=data['unitCode'])
        lecture = Lecture.objects.get(unit=unit,
                                        event_name=data['lectureName'])
        quiz = False
        try:
            #try to retrieve the quiz
            quiz = Quiz.objects.filter(lecture=lecture)[0]
        finally:
            if(quiz):
                quiz_data = {}
                #retrieve all questions and answers for the quiz
                questions = Question.objects.filter(quiz=quiz)
                for question in questions:
                    answer_data = __get_answers(question)
                    quiz_data[question.question] = answer_data
                #convert quiz data to json
                quiz_data = json.dumps(quiz_data)
                return HttpResponse(quiz_data)
            else:
                #the quiz hasn't been created yet
                return HttpResponse("No quiz available")
    else:
        return HttpResponse("Not a valid request", status=400)


def submit_user_answer(request):
    if request.method == 'POST':
        data=json.loads(request.body)
        #retrieve data about the user and quiz
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

        try:
            #is a user answer already exists for a question delete it
            userAnswer = UserAnswer.objects.get(user_email=user_email,
                                                    question=question_object).delete()
        except:
            pass
        
        #create a new user answer in the database
        user_answer = add_user_answer(unit_code, event_name, question, answer, user_email)
        if(user_answer):
            return HttpResponse("Answer Submitted")
        else:
            return HttpResponse("Submission Error")
    else:
        return HttpResponse("Not a valid request", status=400)


def get_quiz_results(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        #retrieve data tp identify the quiz
        unit_code=data['unitCode']
        event_name=data['lectureName']

        unit = Unit.objects.get(unit_code=unit_code)
        lecture = Lecture.objects.get(unit=unit,
                                        event_name=event_name)
        quiz = Quiz.objects.filter(lecture=lecture)[0]

        #retrieve all users enrolled in the unit
        users = UserEnrolledUnit.objects.filter(unit=unit)
        user_performances = {}
        for user in users:
            user_email = user.user.email
            #for each user determine their performance
            user_performance = add_user_quiz_performance(unit_code, event_name, user_email)
            user_performances[user_email] = user_performance.grade
        
        #convert user performance data to json
        user_performances = json.dumps(user_performances)
        return HttpResponse(user_performances)
    else:
        return HttpResponse("Not a valid request", status=400)


def update_quiz(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        #return data about the quiz
        unit_code = data['unitCode']
        event_name = data['lectureName']
        oldQuestion = data['oldQuestion']
        newQuestion = data['newQuestion']
        newAnswers = data['newAnswers']

        unit = Unit.objects.get(unit_code=unit_code)
        lecture = Lecture.objects.get(unit=unit,
                                        event_name=event_name)
        quiz = Quiz.objects.get_or_create(lecture=lecture)[0]

        try:
            #delete the old question
            Question.objects.filter(quiz=quiz, question=oldQuestion).delete()
        finally:
            #add the new question
            question = Question.objects.create(quiz=quiz, question=newQuestion)
        
        for answer in newAnswers.keys():
            #add answers for new question
            is_correct = newAnswers[answer]
            answer = Answer.objects.create(question=question, answer=answer, is_correct=is_correct)

        return HttpResponse("Update succesful")
    else:
        return HttpResponse("Not a valid request", status=400)




'''
Internal Helper Methods
'''

def __get_user_units(user):
    #helper method to return units associated with a user
    if user.is_teacher:
        #teachers are stored within units they teach
        user_units = Unit.objects.filter(teacher=user)
    else:
        #students are stored with their units as user enrolled unit objects
        user_enrolled_units = UserEnrolledUnit.objects.filter(user=user).values('unit')
        user_units = []
        for user_enrolled_unit in user_enrolled_units:
            #retrieves the unit object from each user enrolled unit object
            unit = Unit.objects.get(unit_code=user_enrolled_unit['unit'])
            user_units.append(unit)
    return user_units


def __get_answers(question):
    #helper method to retrieve the answers for a quiz question
    answer_data = {}
    answers = Answer.objects.filter(question=question)
    for answer in answers:
        answer_data[answer.answer] = answer.is_correct
    return answer_data


def __get_unit_data(unit):
    #helper method to return an object containing unit data
    return {
        "unit_code": unit.unit_code,
        "unit_name": unit.unit_name,
        "teacher": unit.teacher.email,
        "unit_enrol_key": unit.unit_enrol_key,
        "number_of_credits": unit.number_of_credits
    }


def __get_assignment_data(assignment):
    #helper method to return an object containing assignment data
    return {
        "unit": assignment.unit.unit_name,
        "unit_code": assignment.unit.unit_code,
        "assignment_name": assignment.event_name,
        #deadline datetime converted to a string
        "deadline": assignment.date_time.strftime("%Y-%m-%dT%H:%M:%S"),
        "weight": assignment.weight
    }


def __get_lecture_data(lecture):
    #helper method to return an object containing lecture data
    return {
        "unit": lecture.unit.unit_name,
        "unit_code": lecture.unit.unit_code,
        "lecture_name": lecture.event_name,
        #lecture datetime converted to a string
        "lecture_time": lecture.date_time.strftime("%Y-%m-%dT%H:%M:%S"),
    }


def __get_submission_data(submission):
    #helper method to return an object containing submission data
    if(submission.submission_time):
        #converts submission datetime to a string
        submission_time = submission.submission_time.strftime("%Y-%m-%dT%H:%M:%S")
    else:
        submission_time = None
    
    #retrieves the name of the submission
    submission_path = submission.submission.name
    submission_path_array = submission_path.split('/')
    submission_name = submission_path_array[-1]
    
    return {
        "user": submission.user.email,
        "submission_name": submission_name,
        "submission_time": submission_time,
        "grade": submission.grade,
        "feedback": submission.feedback
    }


def __get_submission_object(user, assignment):
    #helper method to return a submission object
    try:
        submission = Submission.objects.get(user=user, assignment=assignment)
    except ObjectDoesNotExist:
        #creates a new submission if one does not exist
        submission = Submission.objects.create(user=user, assignment=assignment)
    return submission
