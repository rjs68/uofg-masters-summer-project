import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teach_app.settings')
import django
django.setup()
from datetime import datetime
from teach_app_backend.models import (TeachUser, Unit, UserEnrolledUnit, Assignment, Submission,
                                      Lecture, Quiz, Question, Answer, UserAnswer, UserQuizPerformance)


users = [
    {'email': 'lecturer1@email.com', 'password': 'lecturer1password', 'first_name': 'Lecturer',
        'last_name': 'One', 'is_teacher': True},
    {'email': 'lecturer2@email.com', 'password': 'lecturer2password', 'first_name': 'Lecturer',
        'last_name': 'Two', 'is_teacher': True},
    {'email': 'lecturer3@email.com', 'password': 'lecturer3password', 'first_name': 'Lecturer',
        'last_name': 'Three', 'is_teacher': True},
    {'email': 'student1@email.com', 'password': 'student1password', 'first_name': 'Student',
        'last_name': 'One', 'is_teacher': False},
    {'email': 'student2@email.com', 'password': 'student2password', 'first_name': 'Student',
        'last_name': 'Two', 'is_teacher': False},
    {'email': 'student3@email.com', 'password': 'student3password', 'first_name': 'Student',
        'last_name': 'Three', 'is_teacher': False},
    {'email': 'student4@email.com', 'password': 'student4password', 'first_name': 'Student',
        'last_name': 'Four', 'is_teacher': False},
    {'email': 'student5@email.com', 'password': 'student5password', 'first_name': 'Student',
        'last_name': 'Five', 'is_teacher': False},
]

units = [
    {'unit_code': 1, 'unit_name': 'Unit1', 'teacher': 'lecturer1@email.com', 'credits': 20},
    {'unit_code': 2, 'unit_name': 'Unit2', 'teacher': 'lecturer2@email.com', 'credits': 10},
    {'unit_code': 3, 'unit_name': 'Unit3', 'teacher': 'lecturer3@email.com', 'credits': 15},
]

units_enrolled = [
    {'user': 'student1@email.com', 'unit': 1},
    {'user': 'student1@email.com', 'unit': 2},
    {'user': 'student1@email.com', 'unit': 3},
    {'user': 'student2@email.com', 'unit': 1},
    {'user': 'student2@email.com', 'unit': 2},
    {'user': 'student3@email.com', 'unit': 2},
    {'user': 'student4@email.com', 'unit': 1},
    {'user': 'student4@email.com', 'unit': 2},
    {'user': 'student4@email.com', 'unit': 3},
    {'user': 'student5@email.com', 'unit': 3},
]

assignments = [
    {'unit': 1, 'assignment_name': 'Assign1', 'deadline': datetime(2020, 7, 6, 14), 'weight': 0.2},
    {'unit': 1, 'assignment_name': 'Assign2', 'deadline': datetime(2020, 9, 1, 18), 'weight': 0.1},
    {'unit': 2, 'assignment_name': 'Assign3', 'deadline': datetime(2020, 8, 17, 12), 'weight': 0.2},
    {'unit': 2, 'assignment_name': 'Assign4', 'deadline': datetime(2020, 9, 29, 6), 'weight': 0.5},
    {'unit': 3, 'assignment_name': 'Assign5', 'deadline': datetime(2020, 10, 11, 16), 'weight': 0.3},
]

submissions = [
    {'user': 'student1@email.com', 'unit': 1, 'assignment_name': 'Assign1',
        'submission_time': datetime(2020, 7, 3, 16, 32), 'grade': 20, 'feedback': 'Good'},
    {'user': 'student2@email.com', 'unit': 1, 'assignment_name': 'Assign2',
        'submission_time': datetime(2020, 8, 30, 11, 4), 'grade': 17, 'feedback': 'Good'},
    {'user': 'student3@email.com', 'unit': 2, 'assignment_name': 'Assign3',
        'submission_time': datetime(2020, 8, 17, 13, 30), 'grade': 14, 'feedback': 'Late'},
    {'user': 'student4@email.com', 'unit': 3, 'assignment_name': 'Assign5',
        'submission_time': datetime(2020, 10, 11, 16), 'grade': 21, 'feedback': 'Great'},
    {'user': 'student5@email.com', 'unit': 3, 'assignment_name': 'Assign5',
        'submission_time': datetime(2020, 10, 9, 16, 53), 'grade': 18, 'feedback': 'Good'},
    {'user': 'student1@email.com', 'unit': 2, 'assignment_name': 'Assign4',
        'submission_time': datetime(2020, 9, 20, 22, 10), 'grade': 22, 'feedback': 'Amazing'},
]

lectures = [
    {'unit': 1, 'event_name': 'Lecture1', 'date_time': datetime(2020, 7, 10, 10), 'link': 'link1'},
    {'unit': 1, 'event_name': 'Lecture2', 'date_time': datetime(2020, 7, 17, 10), 'link': 'link2'},
    {'unit': 2, 'event_name': 'Lecture1', 'date_time': datetime(2020, 8, 23, 9), 'link': 'link1'},
    {'unit': 3, 'event_name': 'Lecture1', 'date_time': datetime(2020, 8, 1, 15), 'link': 'link1'},
    {'unit': 3, 'event_name': 'Lecture2', 'date_time': datetime(2020, 7, 30, 16), 'link': 'link1'},
    {'unit': 3, 'event_name': 'Lecture3', 'date_time': datetime(2020, 8, 2, 9), 'link': 'link2'},
    {'unit': 2, 'event_name': 'Lecture2', 'date_time': datetime(2020, 8, 15, 12), 'link': 'link1'},
]

quizzes = [
    {'unit': 1, 'event_name': 'Lecture1', 'total_mark': 10},
    {'unit': 2, 'event_name': 'Lecture1', 'total_mark': 15},
    {'unit': 3, 'event_name': 'Lecture1', 'total_mark': 10},
    {'unit': 3, 'event_name': 'Lecture2', 'total_mark': 20},
]

questions = [
    {'unit': 1, 'event_name': 'Lecture1', 'question': 'Question1'},
    {'unit': 1, 'event_name': 'Lecture1', 'question': 'Question2'},
    {'unit': 1, 'event_name': 'Lecture1', 'question': 'Question3'},
    {'unit': 1, 'event_name': 'Lecture1', 'question': 'Question4'},
    {'unit': 2, 'event_name': 'Lecture1', 'question': 'Question1'},
    {'unit': 2, 'event_name': 'Lecture1', 'question': 'Question2'},
    {'unit': 2, 'event_name': 'Lecture1', 'question': 'Question3'},
    {'unit': 3, 'event_name': 'Lecture1', 'question': 'Question1'},
    {'unit': 3, 'event_name': 'Lecture1', 'question': 'Question2'},
    {'unit': 3, 'event_name': 'Lecture1', 'question': 'Question3'},
    {'unit': 3, 'event_name': 'Lecture2', 'question': 'Question1'},
    {'unit': 3, 'event_name': 'Lecture2', 'question': 'Question2'},
]

answers = [
    {'unit': 1, 'event_name': 'Lecture1', 'question': 'Question1', 'answer': 'Answer1', 'is_correct': True},
    {'unit': 1, 'event_name': 'Lecture1', 'question': 'Question1', 'answer': 'Answer2', 'is_correct': False},
    {'unit': 1, 'event_name': 'Lecture1', 'question': 'Question1', 'answer': 'Answer3', 'is_correct': False},
    {'unit': 1, 'event_name': 'Lecture1', 'question': 'Question2', 'answer': 'Answer1', 'is_correct': False},
    {'unit': 1, 'event_name': 'Lecture1', 'question': 'Question2', 'answer': 'Answer2', 'is_correct': False},
    {'unit': 1, 'event_name': 'Lecture1', 'question': 'Question2', 'answer': 'Answer3', 'is_correct': True},
    {'unit': 1, 'event_name': 'Lecture1', 'question': 'Question2', 'answer': 'Answer4', 'is_correct': False},
    {'unit': 1, 'event_name': 'Lecture1', 'question': 'Question3', 'answer': 'Answer1', 'is_correct': True},
    {'unit': 1, 'event_name': 'Lecture1', 'question': 'Question3', 'answer': 'Answer2', 'is_correct': False},
    {'unit': 1, 'event_name': 'Lecture1', 'question': 'Question4', 'answer': 'Answer1', 'is_correct': False},
    {'unit': 1, 'event_name': 'Lecture1', 'question': 'Question4', 'answer': 'Answer2', 'is_correct': True},
    {'unit': 1, 'event_name': 'Lecture1', 'question': 'Question4', 'answer': 'Answer3', 'is_correct': False},
    {'unit': 2, 'event_name': 'Lecture1', 'question': 'Question1', 'answer': 'Answer1', 'is_correct': True},
    {'unit': 2, 'event_name': 'Lecture1', 'question': 'Question1', 'answer': 'Answer2', 'is_correct': False},
    {'unit': 2, 'event_name': 'Lecture1', 'question': 'Question2', 'answer': 'Answer1', 'is_correct': False},
    {'unit': 2, 'event_name': 'Lecture1', 'question': 'Question2', 'answer': 'Answer2', 'is_correct': False},
    {'unit': 2, 'event_name': 'Lecture1', 'question': 'Question2', 'answer': 'Answer3', 'is_correct': True},
    {'unit': 2, 'event_name': 'Lecture1', 'question': 'Question3', 'answer': 'Answer1', 'is_correct': False},
    {'unit': 2, 'event_name': 'Lecture1', 'question': 'Question3', 'answer': 'Answer2', 'is_correct': False},
    {'unit': 2, 'event_name': 'Lecture1', 'question': 'Question3', 'answer': 'Answer3', 'is_correct': True},
    {'unit': 3, 'event_name': 'Lecture1', 'question': 'Question1', 'answer': 'Answer1', 'is_correct': False},
    {'unit': 3, 'event_name': 'Lecture1', 'question': 'Question1', 'answer': 'Answer2', 'is_correct': True},
    {'unit': 3, 'event_name': 'Lecture1', 'question': 'Question1', 'answer': 'Answer3', 'is_correct': False},
    {'unit': 3, 'event_name': 'Lecture1', 'question': 'Question1', 'answer': 'Answer4', 'is_correct': False},
    {'unit': 3, 'event_name': 'Lecture1', 'question': 'Question2', 'answer': 'Answer1', 'is_correct': True},
    {'unit': 3, 'event_name': 'Lecture1', 'question': 'Question2', 'answer': 'Answer2', 'is_correct': False},
    {'unit': 3, 'event_name': 'Lecture1', 'question': 'Question3', 'answer': 'Answer1', 'is_correct': True},
    {'unit': 3, 'event_name': 'Lecture1', 'question': 'Question3', 'answer': 'Answer2', 'is_correct': False},
    {'unit': 3, 'event_name': 'Lecture1', 'question': 'Question3', 'answer': 'Answer3', 'is_correct': False},
    {'unit': 3, 'event_name': 'Lecture1', 'question': 'Question3', 'answer': 'Answer4', 'is_correct': False},
    {'unit': 3, 'event_name': 'Lecture2', 'question': 'Question1', 'answer': 'Answer1', 'is_correct': False},
    {'unit': 3, 'event_name': 'Lecture2', 'question': 'Question1', 'answer': 'Answer2', 'is_correct': True},
    {'unit': 3, 'event_name': 'Lecture2', 'question': 'Question1', 'answer': 'Answer3', 'is_correct': False},
    {'unit': 3, 'event_name': 'Lecture2', 'question': 'Question2', 'answer': 'Answer1', 'is_correct': False},
    {'unit': 3, 'event_name': 'Lecture2', 'question': 'Question2', 'answer': 'Answer2', 'is_correct': False},
    {'unit': 3, 'event_name': 'Lecture2', 'question': 'Question2', 'answer': 'Answer3', 'is_correct': False},
    {'unit': 3, 'event_name': 'Lecture2', 'question': 'Question2', 'answer': 'Answer4', 'is_correct': True},
]

user_answers = [
    {'unit': 1, 'event_name': 'Lecture1', 'question': 'Question1', 'answer': 'Answer1',
        'user': 'student1@email.com'},
    {'unit': 1, 'event_name': 'Lecture1', 'question': 'Question2', 'answer': 'Answer4',
        'user': 'student1@email.com'},
    {'unit': 1, 'event_name': 'Lecture1', 'question': 'Question3', 'answer': 'Answer1',
        'user': 'student1@email.com'},
    {'unit': 1, 'event_name': 'Lecture1', 'question': 'Question4', 'answer': 'Answer2',
        'user': 'student1@email.com'},
    {'unit': 1, 'event_name': 'Lecture1', 'question': 'Question1', 'answer': 'Answer1',
        'user': 'student2@email.com'},
    {'unit': 1, 'event_name': 'Lecture1', 'question': 'Question2', 'answer': 'Answer3',
        'user': 'student2@email.com'},
    {'unit': 1, 'event_name': 'Lecture1', 'question': 'Question3', 'answer': 'Answer2',
        'user': 'student2@email.com'},
    {'unit': 1, 'event_name': 'Lecture1', 'question': 'Question4', 'answer': 'Answer3',
        'user': 'student2@email.com'},
    {'unit': 2, 'event_name': 'Lecture1', 'question': 'Question1', 'answer': 'Answer2',
        'user': 'student3@email.com'},
    {'unit': 2, 'event_name': 'Lecture1', 'question': 'Question2', 'answer': 'Answer1',
     'user': 'student3@email.com'},
    {'unit': 2, 'event_name': 'Lecture1', 'question': 'Question3', 'answer': 'Answer1',
     'user': 'student3@email.com'},
]

user_quiz_performances = [
    {'unit': 1, 'event_name': 'Lecture1', 'user': 'student1@email.com'},
    {'unit': 1, 'event_name': 'Lecture1', 'user': 'student2@email.com'},
    {'unit': 2, 'event_name': 'Lecture1', 'user': 'student3@email.com'},
]


def populate():
    for user in users:
        add_user(user['email'], user['password'], user['first_name'], user['last_name'], user['is_teacher'])

    for unit in units:
        add_unit(unit['unit_code'], unit['unit_name'], unit['teacher'], unit['credits'])

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


def add_user(email, password, first_name, last_name, is_teacher):
    user = TeachUser.objects.create_user(email=email,
                                         password=password,
                                         first_name=first_name,
                                         last_name=last_name,
                                         is_teacher=is_teacher)


def add_unit(unit_code, unit_name, teacher, number_of_credits):
    teacher_user = TeachUser.objects.get(email=teacher)
    unit = Unit.objects.get_or_create(unit_code=unit_code,
                                      unit_name=unit_name,
                                      teacher=teacher_user,
                                      number_of_credits=number_of_credits)


def add_unit_enrolled(user_email, unit_code):
    user = TeachUser.objects.get(email=user_email)
    unit = Unit.objects.get(unit_code=unit_code)

    unit_enrolled = UserEnrolledUnit.objects.get_or_create(user=user,
                                                            unit=unit)


def add_assignment(unit_code, assignment_name, deadline, weight):
    unit = Unit.objects.get(unit_code=unit_code)
    assignment = Assignment.objects.get_or_create(unit=unit,
                                                  event_name=assignment_name,
                                                  date_time=deadline,
                                                  weight=weight)


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


def add_quiz(unit_code, event_name, total_mark):
    unit = Unit.objects.get(unit_code=unit_code)
    lecture = Lecture.objects.get(unit=unit,
                                  event_name=event_name)
    quiz = Quiz.objects.get_or_create(lecture=lecture,
                                      total_mark=total_mark)


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

    user_answer = UserAnswer.objects.get_or_create(user=user,
                                                   answer=answer)


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

    user_quiz_performance = UserQuizPerformance.objects.get_or_create(user=user,
                                                                      quiz=quiz,
                                                                      grade=user_quiz_grade)


if __name__ == '__main__':
    print('Starting Teach population script...')
    populate()
    print('Teach has been populated!')
