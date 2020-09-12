from django.test import TestCase
from teach_app_backend.models import (University, TeachUser, Unit, Assignment, Submission, Lecture, Quiz, 
                                        Question, Answer, UserAnswer, UserQuizPerformance)
from datetime import datetime
from django.utils.timezone import make_aware

class UnitModelTests(TestCase):
    def test_ensure_unit_code_is_unique(self):
        university = University(university_name="University")
        university.save()
        teacher = TeachUser(email="teacher@email.com", 
                            first_name="teacher", 
                            last_name="teacher", 
                            university=university)
        teacher.save()

        unit1 = Unit(unit_code=1, unit_name="unit1", teacher=teacher, number_of_credits=10)
        unit1.save()
        unit2 = Unit(unit_code=1, unit_name="unit2", teacher=teacher, number_of_credits=10)
        unit2.save()

        self.assertNotEqual(unit1.unit_code, unit2.unit_code)
    
    def test_ensure_number_of_credits_is_positive(self):
        university = University(university_name="University")
        university.save()
        teacher = TeachUser(email="teacher@email.com", 
                            first_name="teacher", 
                            last_name="teacher", 
                            university=university)
        teacher.save()

        unit = Unit(unit_code=1, unit_name="unit", teacher=teacher, number_of_credits=-10)
        unit.save()

        self.assertEqual(unit.number_of_credits>0, True)


class AssignmentModelTest(TestCase):
    def test_ensure_weight_positive(self):
        university = University(university_name="University")
        university.save()
        teacher = TeachUser(email="teacher@email.com", 
                            first_name="teacher", 
                            last_name="teacher", 
                            university=university)
        teacher.save()
        unit = Unit(unit_code=1, unit_name="unit", teacher=teacher, number_of_credits=10)
        unit.save()

        assignment = Assignment(unit=unit, 
                                event_name="Assignment", 
                                date_time=make_aware(datetime.now()), 
                                weight=-0.5)
        assignment.save()

        self.assertEqual(assignment.weight>0, True)
    
    def test_ensure_weight_not_greater_than_one(self):
        university = University(university_name="University")
        university.save()
        teacher = TeachUser(email="teacher@email.com", 
                            first_name="teacher", 
                            last_name="teacher", 
                            university=university)
        teacher.save()
        unit = Unit(unit_code=1, unit_name="unit", teacher=teacher, number_of_credits=10)
        unit.save()

        assignment = Assignment(unit=unit, 
                                event_name="Assignment", 
                                date_time=make_aware(datetime.now()), 
                                weight=1.5)
        assignment.save()

        self.assertEqual(assignment.weight<=1, True)


class SubmissionModelTest(TestCase):
    def test_grade_is_not_negative(self):
        university = University(university_name="University")
        university.save()
        teacher = TeachUser(email="teacher@email.com", 
                            first_name="teacher", 
                            last_name="teacher", 
                            university=university)
        teacher.save()
        unit = Unit(unit_code=1, unit_name="unit", teacher=teacher, number_of_credits=10)
        unit.save()
        assignment = Assignment(unit=unit, 
                                event_name="Assignment", 
                                date_time=make_aware(datetime.now()), 
                                weight=1.5)
        assignment.save()
        student = TeachUser(email="student@email.com", 
                            first_name="student", 
                            last_name="student", 
                            university=university)
        student.save()

        submission = Submission(user=student, assignment=assignment, grade=-10)
        submission.save()

        self.assertEqual(submission.grade>=0, True)
    
    def test_grade_maximum_is_100(self):
        university = University(university_name="University")
        university.save()
        teacher = TeachUser(email="teacher@email.com", 
                            first_name="teacher", 
                            last_name="teacher", 
                            university=university)
        teacher.save()
        unit = Unit(unit_code=1, unit_name="unit", teacher=teacher, number_of_credits=10)
        unit.save()
        assignment = Assignment(unit=unit, 
                                event_name="Assignment", 
                                date_time=make_aware(datetime.now()), 
                                weight=1.5)
        assignment.save()
        student = TeachUser(email="student@email.com", 
                            first_name="student", 
                            last_name="student", 
                            university=university)
        student.save()

        submission = Submission(user=student, assignment=assignment, grade=110)
        submission.save()

        self.assertEqual(submission.grade<=100, True)


class QuizModelTest(TestCase):
    def test_total_mark_is_not_negative(self):
        university = University(university_name="University")
        university.save()
        teacher = TeachUser(email="teacher@email.com", 
                            first_name="teacher", 
                            last_name="teacher", 
                            university=university)
        teacher.save()
        unit = Unit(unit_code=1, unit_name="unit", teacher=teacher, number_of_credits=10)
        unit.save()
        lecture = Lecture(unit=unit, event_name="Lecture", date_time=make_aware(datetime.now()))
        lecture.save()

        quiz = Quiz(lecture=lecture, total_mark=-5)
        quiz.save()

        self.assertEqual(quiz.total_mark>=0, True)
    

    def test_total_mark_is_correct(self):
        university = University(university_name="University")
        university.save()
        teacher = TeachUser(email="teacher@email.com", 
                            first_name="teacher", 
                            last_name="teacher", 
                            university=university)
        teacher.save()
        unit = Unit(unit_code=1, unit_name="unit", teacher=teacher, number_of_credits=10)
        unit.save()
        lecture = Lecture(unit=unit, event_name="Lecture", date_time=make_aware(datetime.now()))
        lecture.save()

        quiz = Quiz(lecture=lecture, total_mark=0)
        quiz.save()
        question1 = Question(quiz=quiz, question="Question1")
        question1.save()
        question2 = Question(quiz=quiz, question="Question2")
        question2.save()

        self.assertEqual(quiz.total_mark==2, True)


class AnswerModelTest(TestCase):
    def test_only_one_correct_answer(self):
        university = University(university_name="University")
        university.save()
        teacher = TeachUser(email="teacher@email.com", 
                            first_name="teacher", 
                            last_name="teacher", 
                            university=university)
        teacher.save()
        unit = Unit(unit_code=1, unit_name="unit", teacher=teacher, number_of_credits=10)
        unit.save()
        lecture = Lecture(unit=unit, event_name="Lecture", date_time=make_aware(datetime.now()))
        lecture.save()
        quiz = Quiz(lecture=lecture, total_mark=0)
        quiz.save()
        question = Question(quiz=quiz, question="Question")
        question.save()

        answer1 = Answer(question=question, answer="Answer1", is_correct=True)
        answer1.save()
        answer2 = Answer(question=question, answer="Answer2", is_correct=True)
        answer2.save()

        self.assertEqual(answer2.is_correct, False)


class UserAnswerModelTest(TestCase):
    def test_only_one_user_answer(self):
        university = University(university_name="University")
        university.save()
        teacher = TeachUser(email="teacher@email.com", 
                            first_name="teacher", 
                            last_name="teacher", 
                            university=university)
        teacher.save()
        unit = Unit(unit_code=1, unit_name="unit", teacher=teacher, number_of_credits=10)
        unit.save()
        lecture = Lecture(unit=unit, event_name="Lecture", date_time=make_aware(datetime.now()))
        lecture.save()
        quiz = Quiz(lecture=lecture, total_mark=0)
        quiz.save()
        question = Question(quiz=quiz, question="Question")
        question.save()
        answer1 = Answer(question=question, answer="Answer1", is_correct=True)
        answer1.save()
        answer2 = Answer(question=question, answer="Answer2", is_correct=True)
        answer2.save()
        student = TeachUser(email="student@email.com", 
                            first_name="student", 
                            last_name="student", 
                            university=university)
        student.save()

        user_answer1 = UserAnswer(user=student, question=question, answer=answer1)
        user_answer1.save()
        user_answer2 = UserAnswer(user=student, question=question, answer=answer2)
        user_answer2.save()
        
        user_answer = UserAnswer.objects.get(user=student, question=question)

        self.assertEqual(user_answer.answer==answer2, True)


class UserQuizPerformanceModelTest(TestCase):
    def test_only_one_quiz_performance(self):
        university = University(university_name="University")
        university.save()
        teacher = TeachUser(email="teacher@email.com", 
                            first_name="teacher", 
                            last_name="teacher", 
                            university=university)
        teacher.save()
        unit = Unit(unit_code=1, unit_name="unit", teacher=teacher, number_of_credits=10)
        unit.save()
        lecture = Lecture(unit=unit, event_name="Lecture", date_time=make_aware(datetime.now()))
        lecture.save()
        quiz = Quiz(lecture=lecture, total_mark=0)
        quiz.save()
        question1 = Question(quiz=quiz, question="Question1")
        question1.save()
        question2 = Question(quiz=quiz, question="Question2")
        question2.save()
        student = TeachUser(email="student@email.com", 
                            first_name="student", 
                            last_name="student", 
                            university=university)
        student.save()

        user_quiz_performance1 = UserQuizPerformance(user=student, quiz=quiz, grade=1)
        user_quiz_performance1.save()
        user_quiz_performance2 = UserQuizPerformance(user=student, quiz=quiz, grade=2)
        user_quiz_performance2.save()

        user_quiz_performance = UserQuizPerformance.objects.get(user=student, quiz=quiz)

        self.assertEqual(user_quiz_performance.grade==2, True)
    
    def test_grade_not_greater_than_total_mark(self):
        university = University(university_name="University")
        university.save()
        teacher = TeachUser(email="teacher@email.com", 
                            first_name="teacher", 
                            last_name="teacher", 
                            university=university)
        teacher.save()
        unit = Unit(unit_code=1, unit_name="unit", teacher=teacher, number_of_credits=10)
        unit.save()
        lecture = Lecture(unit=unit, event_name="Lecture", date_time=make_aware(datetime.now()))
        lecture.save()
        quiz = Quiz(lecture=lecture, total_mark=0)
        quiz.save()
        question1 = Question(quiz=quiz, question="Question1")
        question1.save()
        question2 = Question(quiz=quiz, question="Question2")
        question2.save()
        student = TeachUser(email="student@email.com", 
                            first_name="student", 
                            last_name="student", 
                            university=university)
        student.save()

        user_quiz_performance = UserQuizPerformance(user=student, quiz=quiz, grade=3)
        user_quiz_performance.save()

        self.assertEqual(user_quiz_performance.grade==2, True)
    
    def test_grade_not_less_than_0(self):
        university = University(university_name="University")
        university.save()
        teacher = TeachUser(email="teacher@email.com", 
                            first_name="teacher", 
                            last_name="teacher", 
                            university=university)
        teacher.save()
        unit = Unit(unit_code=1, unit_name="unit", teacher=teacher, number_of_credits=10)
        unit.save()
        lecture = Lecture(unit=unit, event_name="Lecture", date_time=make_aware(datetime.now()))
        lecture.save()
        quiz = Quiz(lecture=lecture, total_mark=0)
        quiz.save()
        question1 = Question(quiz=quiz, question="Question1")
        question1.save()
        question2 = Question(quiz=quiz, question="Question2")
        question2.save()
        student = TeachUser(email="student@email.com", 
                            first_name="student", 
                            last_name="student", 
                            university=university)
        student.save()

        user_quiz_performance = UserQuizPerformance(user=student, quiz=quiz, grade=-1)
        user_quiz_performance.save()

        self.assertEqual(user_quiz_performance.grade==0, True)