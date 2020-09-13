import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teach_app.settings')
import django
from django.core.exceptions import ObjectDoesNotExist
django.setup()
from datetime import datetime
from teach_app_backend.models import (University, TeachUser, Unit, UserEnrolledUnit, Assignment, Submission,
                                      Lecture, Quiz, Question, Answer, UserAnswer, UserQuizPerformance)
from django.utils.timezone import make_aware


universities = [
    {'university_name': 'University of Glasgow', 'teacher_enrol_key': 'uog_teacher',
        'student_enrol_key': 'uog_student'}
]

users = [
    {'email': 'lecturer1@email.com', 'password': 'lecturer1password', 'first_name': 'Lecturer',
        'last_name': 'One', 'university': 'University of Glasgow', 'is_teacher': True},
    {'email': 'lecturer2@email.com', 'password': 'lecturer2password', 'first_name': 'Lecturer',
        'last_name': 'Two', 'university': 'University of Glasgow', 'is_teacher': True},
    {'email': 'lecturer3@email.com', 'password': 'lecturer3password', 'first_name': 'Lecturer',
        'last_name': 'Three', 'university': 'University of Glasgow', 'is_teacher': True},
    {'email': 'student1@email.com', 'password': 'student1password', 'first_name': 'Student',
        'last_name': 'One', 'university': 'University of Glasgow', 'is_teacher': False},
    {'email': 'student2@email.com', 'password': 'student2password', 'first_name': 'Student',
        'last_name': 'Two', 'university': 'University of Glasgow', 'is_teacher': False},
    {'email': 'student3@email.com', 'password': 'student3password', 'first_name': 'Student',
        'last_name': 'Three', 'university': 'University of Glasgow', 'is_teacher': False},
    {'email': 'student4@email.com', 'password': 'student4password', 'first_name': 'Student',
        'last_name': 'Four', 'university': 'University of Glasgow', 'is_teacher': False},
    {'email': 'student5@email.com', 'password': 'student5password', 'first_name': 'Student',
        'last_name': 'Five', 'university': 'University of Glasgow', 'is_teacher': False},
]

units = [
    {'unit_code': 1, 'unit_name': 'Programming', 'teacher': 'lecturer1@email.com',
        'unit_enrol_key': 'programming', 'credits': 20},
    {'unit_code': 2, 'unit_name': 'Databases', 'teacher': 'lecturer2@email.com',
        'unit_enrol_key': 'databases', 'credits': 10},
    {'unit_code': 3, 'unit_name': 'Algorithms', 'teacher': 'lecturer3@email.com',
        'unit_enrol_key': 'algorithms', 'credits': 15},
    {'unit_code': 4, 'unit_name': 'Data Structures', 'teacher': 'lecturer2@email.com',
        'unit_enrol_key': 'datastructures', 'credits': 15},
    {'unit_code': 5, 'unit_name': 'Internet Technology', 'teacher': 'lecturer3@email.com',
        'unit_enrol_key': 'itech', 'credits': 15},
    {'unit_code': 6, 'unit_name': 'Memes', 'teacher': 'lecturer1@email.com',
        'unit_enrol_key': 'memes', 'credits': 60},
]

units_enrolled = [
    {'user': 'student1@email.com', 'unit': 1},
    {'user': 'student1@email.com', 'unit': 2},
    {'user': 'student1@email.com', 'unit': 3},
    {'user': 'student2@email.com', 'unit': 1},
    {'user': 'student2@email.com', 'unit': 2},
    {'user': 'student2@email.com', 'unit': 4},
    {'user': 'student3@email.com', 'unit': 2},
    {'user': 'student3@email.com', 'unit': 4},
    {'user': 'student3@email.com', 'unit': 5},
    {'user': 'student4@email.com', 'unit': 1},
    {'user': 'student4@email.com', 'unit': 2},
    {'user': 'student4@email.com', 'unit': 3},
    {'user': 'student5@email.com', 'unit': 3},
    {'user': 'student5@email.com', 'unit': 5},
]

assignments = [
    {'unit': 1, 'assignment_name': 'Basic Programming', 'deadline': make_aware(datetime(2020, 10, 6, 14)), 
        'weight': 0.2},
    {'unit': 1, 'assignment_name': 'Advanced Programming', 'deadline': make_aware(datetime(2020, 11, 1, 18)), 
        'weight': 0.1},
    {'unit': 2, 'assignment_name': 'Database Normalisation', 'deadline': make_aware(datetime(2020, 10, 17, 12)), 
        'weight': 0.2},
    {'unit': 2, 'assignment_name': 'SQL Statements', 'deadline': make_aware(datetime(2020, 12, 29, 6)), 
        'weight': 0.5},
    {'unit': 3, 'assignment_name': 'Finding O(n)', 'deadline': make_aware(datetime(2020, 10, 11, 16)), 
        'weight': 0.3},
    {'unit': 4, 'assignment_name': 'Structure Design', 'deadline': make_aware(datetime(2020, 10, 11, 16)), 
        'weight': 0.3},
    {'unit': 5, 'assignment_name': 'System Architecture', 'deadline': make_aware(datetime(2020, 10, 11, 16)), 
        'weight': 0.3},
    {'unit': 5, 'assignment_name': 'Application Design', 'deadline': make_aware(datetime(2020, 10, 11, 16)), 
        'weight': 0.3},
    {'unit': 6, 'assignment_name': 'My Favourite Meme', 'deadline': make_aware(datetime(2020, 9, 14, 18)), 
        'weight': 1},
]

submissions = []
# submissions = [
#     {'user': 'student1@email.com', 'unit': 1, 'assignment_name': 'Basic Programming',
#         'submission_time': datetime(2020, 7, 3, 16, 32), 'grade': 20, 'feedback': 'Good'},
#     {'user': 'student2@email.com', 'unit': 1, 'assignment_name': 'Assign2',
#         'submission_time': datetime(2020, 8, 30, 11, 4), 'grade': 17, 'feedback': 'Good'},
#     {'user': 'student3@email.com', 'unit': 2, 'assignment_name': 'Assign3',
#         'submission_time': datetime(2020, 8, 17, 13, 30), 'grade': 14, 'feedback': 'Late'},
#     {'user': 'student4@email.com', 'unit': 3, 'assignment_name': 'Assign5',
#         'submission_time': datetime(2020, 10, 11, 16), 'grade': 21, 'feedback': 'Great'},
#     {'user': 'student5@email.com', 'unit': 3, 'assignment_name': 'Assign5',
#         'submission_time': datetime(2020, 10, 9, 16, 53), 'grade': 18, 'feedback': 'Good'},
#     {'user': 'student1@email.com', 'unit': 2, 'assignment_name': 'Assign4',
#         'submission_time': datetime(2020, 9, 20, 22, 10), 'grade': 22, 'feedback': 'Amazing'},
# ]

lectures = [
    {'unit': 1, 'event_name': 'Introduction to Programming', 'date_time': make_aware(datetime(2020, 10, 10, 10)), 
        'link': 'link1'},
    {'unit': 1, 'event_name': 'Object Orientated Programming', 'date_time': make_aware(datetime(2020, 10, 17, 10)), 
        'link': 'link1'},
    {'unit': 2, 'event_name': 'Entities and Relationships', 'date_time': make_aware(datetime(2020, 11, 23, 9)), 
        'link': 'link1'},
    {'unit': 3, 'event_name': 'Algorithms in the Real World', 'date_time': make_aware(datetime(2020, 12, 1, 15)), 
        'link': 'link1'},
    {'unit': 3, 'event_name': 'Designing Algorithms', 'date_time': make_aware(datetime(2020, 11, 30, 16)), 
        'link': 'link1'},
    {'unit': 3, 'event_name': 'Analysis Algorithm Efficiency', 'date_time': make_aware(datetime(2020, 10, 2, 9)), 
        'link': 'link2'},
    {'unit': 4, 'event_name': 'Introduction to Data Structure', 'date_time': make_aware(datetime(2020, 11, 15, 12)), 
        'link': 'link1'},
    {'unit': 4, 'event_name': 'Choosing a Data Structure', 'date_time': make_aware(datetime(2020, 11, 21, 12)), 
        'link': 'link1'},
    {'unit': 5, 'event_name': 'What is the Internet?', 'date_time': make_aware(datetime(2020, 11, 15, 12)), 
        'link': 'link1'},
    {'unit': 5, 'event_name': 'Designing Web Applications', 'date_time': make_aware(datetime(2020, 11, 24, 12)), 
        'link': 'link1'},
    {'unit': 6, 'event_name': 'Introduction to Memes', 'date_time': make_aware(datetime(2020, 11, 15, 12)), 
        'link': 'link1'},
    {'unit': 6, 'event_name': 'Obtaining Memes from Reliable Sources', 'date_time': make_aware(datetime(2020, 11, 27, 12)), 
        'link': 'link1'},
    {'unit': 6, 'event_name': 'Analysing the Comedy Value of a Meme', 'date_time': make_aware(datetime(2020, 12, 7, 12)), 
        'link': 'link1'},
]

quizzes = [
    {'unit': 1, 'event_name': 'Introduction to Programming', 'total_mark': 0},
    {'unit': 2, 'event_name': 'Entities and Relationships', 'total_mark': 0},
    {'unit': 3, 'event_name': 'Algorithms in the Real World', 'total_mark': 0},
    {'unit': 3, 'event_name': 'Designing Algorithms', 'total_mark': 0},
]

questions = [
    {'unit': 1, 'event_name': 'Introduction to Programming', 'question': 'How cool is programming?'},
    {'unit': 1, 'event_name': 'Introduction to Programming', 'question': 'Is programming hard?'},
    {'unit': 1, 'event_name': 'Introduction to Programming', 'question': 'How long will this course last?'},
    {'unit': 2, 'event_name': 'Entities and Relationships', 'question': 'What is an entity?'},
    {'unit': 2, 'event_name': 'Entities and Relationships', 'question': 'What is a relationship?'},
    {'unit': 2, 'event_name': 'Entities and Relationships', 'question': 'How do we display entities and relationships?'},
    {'unit': 3, 'event_name': 'Algorithms in the Real World', 'question': 'Can we compare an algorithm to a shopping trip?'},
    {'unit': 3, 'event_name': 'Algorithms in the Real World', 'question': 'What is an algorithm?'},
    {'unit': 3, 'event_name': 'Algorithms in the Real World', 'question': 'Are algorithms useful?'},
    {'unit': 3, 'event_name': 'Designing Algorithms', 'question': 'How should we start designing an algorithm?'},
    {'unit': 3, 'event_name': 'Designing Algorithms', 'question': 'Does algorithm design require coding?'},
]

answers = [
    {'unit': 1, 'event_name': 'Introduction to Programming', 'question': 'How cool is programming?', 
        'answer': 'Very Cool', 'is_correct': True},
    {'unit': 1, 'event_name': 'Introduction to Programming', 'question': 'How cool is programming?', 
        'answer': 'Kinda Cool', 'is_correct': False},
    {'unit': 1, 'event_name': 'Introduction to Programming', 'question': 'How cool is programming?', 
        'answer': 'Not Cool', 'is_correct': False},
    {'unit': 1, 'event_name': 'Introduction to Programming', 'question': 'Is programming hard?', 
        'answer': 'Yes', 'is_correct': False},
    {'unit': 1, 'event_name': 'Introduction to Programming', 'question': 'Is programming hard?', 
        'answer': 'No', 'is_correct': False},
    {'unit': 1, 'event_name': 'Introduction to Programming', 'question': 'Is programming hard?', 
        'answer': 'Maybe', 'is_correct': True},
    {'unit': 1, 'event_name': 'Introduction to Programming', 'question': 'Is programming hard?', 
        'answer': 'Not Sure', 'is_correct': False},
    {'unit': 1, 'event_name': 'Introduction to Programming', 'question': 'How long will this course last?', 
        'answer': '6 months', 'is_correct': True},
    {'unit': 1, 'event_name': 'Introduction to Programming', 'question': 'How long will this course last?', 
        'answer': 'Until the end of time', 'is_correct': False},
    {'unit': 2, 'event_name': 'Entities and Relationships', 'question': 'What is an entity?',
        'answer': 'A representation of a real thing', 'is_correct': True},
    {'unit': 2, 'event_name': 'Entities and Relationships', 'question': 'What is an entity?', 
        'answer': 'A random thing some guy made up', 'is_correct': False},
    {'unit': 2, 'event_name': 'Entities and Relationships', 'question': 'What is a relationship?', 
        'answer': 'A connection between entities', 'is_correct': True},
    {'unit': 2, 'event_name': 'Entities and Relationships', 'question': 'What is a relationship?', 
        'answer': 'Love', 'is_correct': False},
    {'unit': 2, 'event_name': 'Entities and Relationships', 'question': 'What is a relationship?', 
        'answer': 'A social construct', 'is_correct': False},
    {'unit': 2, 'event_name': 'Entities and Relationships', 'question': 'How do we display entities and relationships?', 
        'answer': 'A pretty crayon drawing', 'is_correct': False},
    {'unit': 2, 'event_name': 'Entities and Relationships', 'question': 'How do we display entities and relationships?', 
        'answer': 'A playdough model', 'is_correct': False},
    {'unit': 2, 'event_name': 'Entities and Relationships', 'question': 'How do we display entities and relationships?', 
        'answer': 'An ER diagram', 'is_correct': True},
    {'unit': 3, 'event_name': 'Algorithms in the Real World', 'question': 'Can we compare an algorithm to a shopping trip?', 
        'answer': 'Ummmm..... what?', 'is_correct': False},
    {'unit': 3, 'event_name': 'Algorithms in the Real World', 'question': 'Can we compare an algorithm to a shopping trip?', 
        'answer': 'Yes, of course', 'is_correct': True},
    {'unit': 3, 'event_name': 'Algorithms in the Real World', 'question': 'Can we compare an algorithm to a shopping trip?', 
        'answer': 'No, don\'t be stupid', 'is_correct': False},
    {'unit': 3, 'event_name': 'Algorithms in the Real World', 'question': 'What is an algorithm?', 
        'answer': 'Some really confusing technical things', 'is_correct': False},
    {'unit': 3, 'event_name': 'Algorithms in the Real World', 'question': 'What is an algorithm?', 
        'answer': 'A set of steps to complete a task', 'is_correct': True},
    {'unit': 3, 'event_name': 'Algorithms in the Real World', 'question': 'Are algorithms useful?', 
        'answer': 'Generally, unless written by the UK government to determine A-Level results', 'is_correct': True},
    {'unit': 3, 'event_name': 'Algorithms in the Real World', 'question': 'Are algorithms useful?', 
        'answer': 'Yes', 'is_correct': False},
    {'unit': 3, 'event_name': 'Algorithms in the Real World', 'question': 'Are algorithms useful?', 
        'answer': 'No', 'is_correct': False},
    {'unit': 3, 'event_name': 'Algorithms in the Real World', 'question': 'Are algorithms useful?', 
        'answer': 'Maybe', 'is_correct': False},
    {'unit': 3, 'event_name': 'Designing Algorithms', 'question': 'How should we start designing an algorithm?', 
        'answer': 'Just start coding it and hope for the best', 'is_correct': False},
    {'unit': 3, 'event_name': 'Designing Algorithms', 'question': 'How should we start designing an algorithm?', 
        'answer': 'Don\'t bother, it sounds too hard', 'is_correct': False},
    {'unit': 3, 'event_name': 'Designing Algorithms', 'question': 'How should we start designing an algorithm?', 
        'answer': 'Write down the steps using pen and paper', 'is_correct': True},
    {'unit': 3, 'event_name': 'Designing Algorithms', 'question': 'Does algorithm design require coding?', 
        'answer': 'Yes', 'is_correct': False},
    {'unit': 3, 'event_name': 'Designing Algorithms', 'question': 'Does algorithm design require coding?', 
        'answer': 'Some', 'is_correct': False},
    {'unit': 3, 'event_name': 'Designing Algorithms', 'question': 'Does algorithm design require coding?', 
        'answer': 'None', 'is_correct': True},
]

user_answers = []
# user_answers = [
#     {'unit': 1, 'event_name': 'Introduction to Programming', 'question': 'Question1', 'answer': 'Answer1',
#         'user': 'student1@email.com'},
#     {'unit': 1, 'event_name': 'Introduction to Programming', 'question': 'Question2', 'answer': 'Answer4',
#         'user': 'student1@email.com'},
#     {'unit': 1, 'event_name': 'Introduction to Programming', 'question': 'Question3', 'answer': 'Answer1',
#         'user': 'student1@email.com'},
#     {'unit': 1, 'event_name': 'Introduction to Programming', 'question': 'Question4', 'answer': 'Answer2',
#         'user': 'student1@email.com'},
#     {'unit': 1, 'event_name': 'Introduction to Programming', 'question': 'Question1', 'answer': 'Answer1',
#         'user': 'student2@email.com'},
#     {'unit': 1, 'event_name': 'Introduction to Programming', 'question': 'Question2', 'answer': 'Answer3',
#         'user': 'student2@email.com'},
#     {'unit': 1, 'event_name': 'Lecture1', 'question': 'Question3', 'answer': 'Answer2',
#         'user': 'student2@email.com'},
#     {'unit': 1, 'event_name': 'Lecture1', 'question': 'Question4', 'answer': 'Answer3',
#         'user': 'student2@email.com'},
#     {'unit': 2, 'event_name': 'Lecture1', 'question': 'Question1', 'answer': 'Answer2',
#         'user': 'student3@email.com'},
#     {'unit': 2, 'event_name': 'Lecture1', 'question': 'Question2', 'answer': 'Answer1',
#      'user': 'student3@email.com'},
#     {'unit': 2, 'event_name': 'Lecture1', 'question': 'Question3', 'answer': 'Answer1',
#      'user': 'student3@email.com'},
# ]

user_quiz_performances = []
# user_quiz_performances = [
#     {'unit': 1, 'event_name': 'Lecture1', 'user': 'student1@email.com'},
#     {'unit': 1, 'event_name': 'Lecture1', 'user': 'student2@email.com'},
#     {'unit': 2, 'event_name': 'Lecture1', 'user': 'student3@email.com'},
# ]


def populate():
    for university in universities:
        add_university(university['university_name'], university['teacher_enrol_key'],
                       university['student_enrol_key'])
    
    university = University.objects.get(university_name="University of Glasgow")
    admin = TeachUser.objects.create_superuser(email="admin@email.com",
                                                password="adminpassword",
                                                first_name="admin",
                                                last_name="admin",
                                                university=university,
                                                is_teacher=True)


    for user in users:
        add_user(user['email'], user['password'], user['first_name'], user['last_name'],
                 user['university'], user['is_teacher'])

    for unit in units:
        add_unit(unit['unit_code'], unit['unit_name'], unit['teacher'], unit['unit_enrol_key'],
                 unit['credits'])

    for unit_enrolled in units_enrolled:
        add_unit_enrolled(unit_enrolled['user'], unit_enrolled['unit'])

    for assignment in assignments:
        add_assignment(assignment['unit'], assignment['assignment_name'], assignment['deadline'],
                       assignment['weight'])

    for submission in submissions:
        add_submission(submission['user'], submission['unit'], submission['assignment_name'],
                       submission['submission_time'], submission['grade'], submission['feedback'])

    for lecture in lectures:
        add_lecture(lecture['unit'], lecture['event_name'], lecture['date_time'], lecture['link'])

    for quiz in quizzes:
        add_quiz(quiz['unit'], quiz['event_name'], quiz['total_mark'])

    for question in questions:
        add_question(question['unit'], question['event_name'], question['question'])

    for answer in answers:
        add_answer(answer['unit'], answer['event_name'], answer['question'], answer['answer'],
                   answer['is_correct'])

    for user_answer in user_answers:
        add_user_answer(user_answer['unit'], user_answer['event_name'], user_answer['question'],
                        user_answer['answer'], user_answer['user'])

    for user in user_quiz_performances:
        add_user_quiz_performance(user['unit'], user['event_name'], user['user'])


def add_university(university_name, teacher_enrol_key, student_enrol_key): 
    university = University.objects.get_or_create(university_name=university_name,
                                                  teacher_enrol_key=teacher_enrol_key,
                                                  student_enrol_key=student_enrol_key)


def add_user(email, password, first_name, last_name, university_name, is_teacher):
    university = University.objects.get(university_name=university_name)
    user = TeachUser.objects.create_user(email=email,
                                         password=password,
                                         first_name=first_name,
                                         last_name=last_name,
                                         university=university,
                                         is_teacher=is_teacher)
    
    return user


def add_unit(unit_code, unit_name, teacher, unit_enrol_key, number_of_credits):
    teacher_user = TeachUser.objects.get(email=teacher)
    unit = Unit.objects.get_or_create(unit_code=unit_code,
                                      unit_name=unit_name,
                                      teacher=teacher_user,
                                      unit_enrol_key=unit_enrol_key,
                                      number_of_credits=number_of_credits)

    return unit


def add_unit_enrolled(user_email, unit_code):
    user = TeachUser.objects.get(email=user_email)
    unit = Unit.objects.get(unit_code=unit_code)

    unit_enrolled = UserEnrolledUnit.objects.get_or_create(user=user,
                                                            unit=unit)
    
    return unit_enrolled


def add_assignment(unit_code, assignment_name, deadline, weight):
    unit = Unit.objects.get(unit_code=unit_code)
    assignment = Assignment.objects.get_or_create(unit=unit,
                                                  event_name=assignment_name,
                                                  date_time=deadline,
                                                  weight=weight)
    
    return assignment


def add_submission(user_email, unit_code, assignment_name, submission_time, grade, feedback):
    user = TeachUser.objects.get(email=user_email)
    unit = Unit.objects.get(unit_code=unit_code)
    assignment = Assignment.objects.get(unit=unit,
                                        event_name=assignment_name)
    submission = Submission.objects.get_or_create(user=user,
                                                  assignment=assignment,
                                                  submission_time=submission_time,
                                                  grade=grade,
                                                  feedback=feedback)


def add_lecture(unit_code, event_name, date_time, link):
    unit = Unit.objects.get(unit_code=unit_code)
    lecture = Lecture.objects.get_or_create(unit=unit,
                                            event_name=event_name,
                                            date_time=date_time,
                                            link=link)
    
    return lecture


def add_quiz(unit_code, event_name, total_mark):
    unit = Unit.objects.get(unit_code=unit_code)
    lecture = Lecture.objects.get(unit=unit,
                                  event_name=event_name)
    quiz = Quiz.objects.get_or_create(lecture=lecture,
                                      total_mark=total_mark)
    
    return quiz


def add_question(unit_code, event_name, question):
    unit = Unit.objects.get(unit_code=unit_code)
    lecture = Lecture.objects.get(unit=unit,
                                  event_name=event_name)
    quiz = Quiz.objects.get(lecture=lecture)
    question = Question.objects.get_or_create(quiz=quiz,
                                              question=question)


def add_answer(unit_code, event_name, question, answer, is_correct):
    unit = Unit.objects.get(unit_code=unit_code)
    lecture = Lecture.objects.get(unit=unit,
                                  event_name=event_name)
    quiz = Quiz.objects.get(lecture=lecture)
    question = Question.objects.get(quiz=quiz,
                                    question=question)
    answer = Answer.objects.get_or_create(question=question,
                                          answer=answer,
                                          is_correct=is_correct)


def add_user_answer(unit_code, event_name, question, answer, user_email):
    unit = Unit.objects.get(unit_code=unit_code)
    lecture = Lecture.objects.get(unit=unit,
                                  event_name=event_name)
    quiz = Quiz.objects.get(lecture=lecture)
    question = Question.objects.get(quiz=quiz,
                                    question=question)
    answer = Answer.objects.get(question=question,
                                answer=answer)
    user = TeachUser.objects.get(email=user_email)

    try:
        user_answer = UserAnswer.objects.get(user=user,
                                            question=question)
        user_answer.answer = answer
        user_answer.save()
    except ObjectDoesNotExist:
        user_answer = UserAnswer.objects.create(user=user,
                                                question=question,
                                                answer=answer)
    
    return user_answer


def add_user_quiz_performance(unit_code, event_name, user_email):
    unit = Unit.objects.get(unit_code=unit_code)
    lecture = Lecture.objects.get(unit=unit,
                                  event_name=event_name)
    quiz = Quiz.objects.get(lecture=lecture)
    user = TeachUser.objects.get(email=user_email)

    quiz_questions = Question.objects.filter(quiz=quiz)
    quiz_answers = []
    for question in quiz_questions:
        question_answers = Answer.objects.filter(question=question)
        for answer in question_answers:
            quiz_answers.append(answer)

    user_quiz_grade = 0
    for answer in quiz_answers:
        if UserAnswer.objects.filter(user=user, answer=answer).count() > 0 and answer.is_correct:
            user_quiz_grade += 1

    try:
        user_quiz_performance = UserQuizPerformance.objects.get(user=user,
                                                                quiz=quiz)
        user_quiz_performance.grade = user_quiz_grade
        user_quiz_performance.save()
    except ObjectDoesNotExist:
        user_quiz_performance = UserQuizPerformance.objects.create(user=user,
                                                                    quiz=quiz,
                                                                    grade=user_quiz_grade)

    return user_quiz_performance


if __name__ == '__main__':
    print('Starting Teach population script...')
    populate()
    print('Teach has been populated!')
