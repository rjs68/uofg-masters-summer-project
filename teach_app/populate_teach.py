import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teach_app.settings')
import django
django.setup()
from datetime import datetime
from django.contrib.auth.models import User
from teach_app_backend.models import (TeachUser, Unit, Event, Assignment, Submission, Lecture,
                                      Quiz, Question, Answer, UserAnswer, UserQuizPerformance)
from teach_app_backend.managers import TeachUserManager


users = [
    {'email': 'lecturer1@email.com', 'first_name': 'Lecturer', 'last_name': 'One', 'is_teacher': True},
    {'email': 'lecturer2@email.com', 'first_name': 'Lecturer', 'last_name': 'Two', 'is_teacher': True},
    {'email': 'lecturer3@email.com', 'first_name': 'Lecturer', 'last_name': 'Three', 'is_teacher': True},
    {'email': 'student1@email.com', 'first_name': 'Student', 'last_name': 'One', 'is_teacher': False},
    {'email': 'student2@email.com', 'first_name': 'Student', 'last_name': 'Two', 'is_teacher': False},
    {'email': 'student3@email.com', 'first_name': 'Student', 'last_name': 'Three', 'is_teacher': False},
    {'email': 'student4@email.com', 'first_name': 'Student', 'last_name': 'Four', 'is_teacher': False},
    {'email': 'student5@email.com', 'first_name': 'Student', 'last_name': 'Five', 'is_teacher': False},
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
    {'unit': 4, 'event_name': 'Lecture1', 'date_time': datetime(2020, 7, 30, 16), 'link': 'link1'},
    {'unit': 4, 'event_name': 'Lecture2', 'date_time': datetime(2020, 8, 2, 9), 'link': 'link2'},
    {'unit': 5, 'event_name': 'Lecture1', 'date_time': datetime(2020, 8, 15, 12), 'link': 'link1'},
]

quizzes = [
    {'unit': 1, 'event_name': 'Lecture1', 'total_mark': 10},
    {'unit': 2, 'event_name': 'Lecture1', 'total_mark': 15},
    {'unit': 3, 'event_name': 'Lecture1', 'total_mark': 10},
    {'unit': 4, 'event_name': 'Lecture2', 'total_mark': 20},
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
    {'unit': 4, 'event_name': 'Lecture2', 'question': 'Question1'},
    {'unit': 4, 'event_name': 'Lecture2', 'question': 'Question2'},
]

answers = [
    {'unit': 1, 'event_name': 'Lecture1', 'question': 'Question1', 'answer': 'Answer1', 'isCorrect': True},
    {'unit': 1, 'event_name': 'Lecture1', 'question': 'Question1', 'answer': 'Answer2', 'isCorrect': False},
    {'unit': 1, 'event_name': 'Lecture1', 'question': 'Question1', 'answer': 'Answer3', 'isCorrect': False},
    {'unit': 1, 'event_name': 'Lecture1', 'question': 'Question2', 'answer': 'Answer1', 'isCorrect': False},
    {'unit': 1, 'event_name': 'Lecture1', 'question': 'Question2', 'answer': 'Answer2', 'isCorrect': False},
    {'unit': 1, 'event_name': 'Lecture1', 'question': 'Question2', 'answer': 'Answer3', 'isCorrect': True},
    {'unit': 1, 'event_name': 'Lecture1', 'question': 'Question2', 'answer': 'Answer4', 'isCorrect': False},
    {'unit': 1, 'event_name': 'Lecture1', 'question': 'Question3', 'answer': 'Answer1', 'isCorrect': True},
    {'unit': 1, 'event_name': 'Lecture1', 'question': 'Question3', 'answer': 'Answer2', 'isCorrect': False},
    {'unit': 1, 'event_name': 'Lecture1', 'question': 'Question4', 'answer': 'Answer1', 'isCorrect': False},
    {'unit': 1, 'event_name': 'Lecture1', 'question': 'Question4', 'answer': 'Answer2', 'isCorrect': True},
    {'unit': 1, 'event_name': 'Lecture1', 'question': 'Question4', 'answer': 'Answer3', 'isCorrect': False},
    {'unit': 2, 'event_name': 'Lecture1', 'question': 'Question1', 'answer': 'Answer1', 'isCorrect': True},
    {'unit': 2, 'event_name': 'Lecture1', 'question': 'Question1', 'answer': 'Answer2', 'isCorrect': False},
    {'unit': 2, 'event_name': 'Lecture1', 'question': 'Question2', 'answer': 'Answer1', 'isCorrect': False},
    {'unit': 2, 'event_name': 'Lecture1', 'question': 'Question2', 'answer': 'Answer2', 'isCorrect': False},
    {'unit': 2, 'event_name': 'Lecture1', 'question': 'Question2', 'answer': 'Answer3', 'isCorrect': True},
    {'unit': 2, 'event_name': 'Lecture1', 'question': 'Question3', 'answer': 'Answer1', 'isCorrect': False},
    {'unit': 2, 'event_name': 'Lecture1', 'question': 'Question3', 'answer': 'Answer2', 'isCorrect': False},
    {'unit': 2, 'event_name': 'Lecture1', 'question': 'Question3', 'answer': 'Answer3', 'isCorrect': True},
    {'unit': 3, 'event_name': 'Lecture1', 'question': 'Question1', 'answer': 'Answer1', 'isCorrect': False},
    {'unit': 3, 'event_name': 'Lecture1', 'question': 'Question1', 'answer': 'Answer2', 'isCorrect': True},
    {'unit': 3, 'event_name': 'Lecture1', 'question': 'Question1', 'answer': 'Answer3', 'isCorrect': False},
    {'unit': 3, 'event_name': 'Lecture1', 'question': 'Question1', 'answer': 'Answer4', 'isCorrect': False},
    {'unit': 3, 'event_name': 'Lecture1', 'question': 'Question2', 'answer': 'Answer1', 'isCorrect': True},
    {'unit': 3, 'event_name': 'Lecture1', 'question': 'Question2', 'answer': 'Answer2', 'isCorrect': False},
    {'unit': 3, 'event_name': 'Lecture1', 'question': 'Question3', 'answer': 'Answer1', 'isCorrect': True},
    {'unit': 3, 'event_name': 'Lecture1', 'question': 'Question3', 'answer': 'Answer2', 'isCorrect': False},
    {'unit': 3, 'event_name': 'Lecture1', 'question': 'Question3', 'answer': 'Answer3', 'isCorrect': False},
    {'unit': 3, 'event_name': 'Lecture1', 'question': 'Question3', 'answer': 'Answer4', 'isCorrect': False},
    {'unit': 4, 'event_name': 'Lecture2', 'question': 'Question1', 'answer': 'Answer1', 'isCorrect': False},
    {'unit': 4, 'event_name': 'Lecture2', 'question': 'Question1', 'answer': 'Answer2', 'isCorrect': True},
    {'unit': 4, 'event_name': 'Lecture2', 'question': 'Question1', 'answer': 'Answer3', 'isCorrect': False},
    {'unit': 4, 'event_name': 'Lecture2', 'question': 'Question2', 'answer': 'Answer1', 'isCorrect': False},
    {'unit': 4, 'event_name': 'Lecture2', 'question': 'Question2', 'answer': 'Answer2', 'isCorrect': False},
    {'unit': 4, 'event_name': 'Lecture2', 'question': 'Question2', 'answer': 'Answer3', 'isCorrect': False},
    {'unit': 4, 'event_name': 'Lecture2', 'question': 'Question2', 'answer': 'Answer4', 'isCorrect': True},
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

user_quiz_performance = [
    {'unit': 1, 'event_name': 'Lecture1', 'user': 'student1@email.com'},
    {'unit': 1, 'event_name': 'Lecture1', 'user': 'student2@email.com'},
    {'unit': 2, 'event_name': 'Lecture1', 'user': 'student3@email.com'},
]
