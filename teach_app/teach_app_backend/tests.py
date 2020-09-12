from django.test import TestCase, Client
from teach_app_backend.models import (University, TeachUser, Unit, Assignment, Submission, Lecture, Quiz, 
                                        Question, Answer, UserAnswer, UserQuizPerformance, UserEnrolledUnit)
from datetime import datetime
from django.utils.timezone import make_aware
import simplejson as json

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


class LoginSignupTest(TestCase):
    def test_ensure_post_request(self):
        client = Client()

        response = client.get('/login/')
        self.assertEqual(response.status_code, 400)
    
        response = client.get('/signup/')
        self.assertEqual(response.status_code, 400)
    
    def test_teacher_login(self):
        university = University(university_name="University")
        university.save()
        teacher = TeachUser(email="teacher@email.com", 
                            first_name="teacher", 
                            last_name="teacher", 
                            university=university,
                            is_teacher=True)
        teacher.set_password("teacherpassword")
        teacher.save()

        client = Client()
        login_info = {}
        login_info["email"] = "teacher@email.com"
        login_info["password"] = "teacherpassword"

        response = client.post('/login/', content_type='application/json', data=login_info)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Teacher Login Successful")

        login_info["password"] = "studentpassword"

        response = client.post('/login/', content_type='application/json', data=login_info)
        self.assertEqual(response.status_code, 401)
    
    def test_student_login(self):
        university = University(university_name="University")
        university.save()
        student = TeachUser(email="student@email.com", 
                            first_name="student", 
                            last_name="student", 
                            university=university,
                            is_teacher=False)
        student.set_password("studentpassword")
        student.save()

        client = Client()
        login_info = {
            "email": "student@email.com",
            "password": "studentpassword"
        }

        response = client.post('/login/', content_type='application/json', data=login_info)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Student Login Successful")

        login_info["password"] = "teacherpassword"

        response = client.post('/login/', content_type='application/json', data=login_info)

        self.assertEqual(response.status_code, 401)
    
    def test_teacher_signup(self):
        university = University(university_name="University", teacher_enrol_key="teacherenrol")
        university.save()

        client = Client()
        signup_info = {
            "enrolmentKey": "teacherenrol",
            "email": "teacher@email.com",
            "password": "teacherpassword",
            "firstName": "teacher",
            "lastName": "teacher"
        }
        
        response = client.post('/signup/', content_type='application/json', data=signup_info)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Teacher Creation Successful")

        signup_info["enrolmentKey"] = "studentenrol"

        response = client.post('/signup/', content_type='application/json', data=signup_info)

        self.assertEqual(response.status_code, 401)
    
    def test_student_signup(self):
        university = University(university_name="University", student_enrol_key="studentenrol")
        university.save()

        client = Client()
        signup_info = {
            "enrolmentKey": "studentenrol",
            "email": "student@email.com",
            "password": "studentpassword",
            "firstName": "student",
            "lastName": "student"
        }
        
        response = client.post('/signup/', content_type='application/json', data=signup_info)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Student Creation Successful")

        signup_info["enrolmentKey"] = "teacherenrol"

        response = client.post('/signup/', content_type='application/json', data=signup_info)

        self.assertEqual(response.status_code, 401)


class UnitFunctionalityTest(TestCase):
    def test_ensure_post_request(self):
        client = Client()

        response = client.get('/units/')
        self.assertEqual(response.status_code, 400)

        response = client.get('/create-unit/')
        self.assertEqual(response.status_code, 400)

        response = client.get('/unit-enrol/')
        self.assertEqual(response.status_code, 400)
    
    def test_get_correct_user_units(self):
        university = University(university_name="University")
        university.save()
        teacher = TeachUser(email="teacher@email.com", 
                            first_name="teacher", 
                            last_name="teacher", 
                            university=university,
                            is_teacher=True)
        teacher.save()
        unit = Unit(unit_code=1, unit_name="unit", teacher=teacher, unit_enrol_key="enrol", number_of_credits=10)
        unit.save()
        student = TeachUser(email="student@email.com", 
                            first_name="student", 
                            last_name="student", 
                            university=university,
                            is_teacher=False)
        student.save()
        user_enrolled_unit = UserEnrolledUnit(user=student, unit=unit)
        user_enrolled_unit.save()

        client = Client()
        user_info = {
            "email": "student@email.com"
        }

        response = client.post('/units/', content_type='application/json', data=user_info)

        expected_response = [{
            "unit_code": 1,
            "unit_name": "unit",
            "teacher": "teacher@email.com",
            "unit_enrol_key": "enrol",
            "number_of_credits": 10
        }]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), expected_response)
    
    def test_unit_creation(self):
        university = University(university_name="University")
        university.save()
        teacher = TeachUser(email="teacher@email.com", 
                            first_name="teacher", 
                            last_name="teacher", 
                            university=university,
                            is_teacher=True)
        teacher.save()

        client = Client()
        unit_info = {
            "unitCode": 1,
            "unitName": "unit",
            "teacher": "teacher@email.com",
            "unitEnrolmentKey": "enrol",
            "numberOfCredits": 10
        }

        response = client.post('/create-unit/', content_type='application/json', data=unit_info)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Unit Created Successfully")
    
    def test_unit_enrollment(self):
        university = University(university_name="University")
        university.save()
        teacher = TeachUser(email="teacher@email.com", 
                            first_name="teacher", 
                            last_name="teacher", 
                            university=university,
                            is_teacher=True)
        teacher.save()
        unit = Unit(unit_code=1, unit_name="unit", teacher=teacher, unit_enrol_key="enrol", number_of_credits=10)
        unit.save()
        student = TeachUser(email="student@email.com", 
                            first_name="student", 
                            last_name="student", 
                            university=university,
                            is_teacher=False)
        student.save()

        client = Client()
        enrollment_info = {
            "unitEnrolmentKey": "enrol",
            "email": "student@email.com",
            "unitCode": 1
        }

        response = client.post('/unit-enrol/', content_type='application/json', data=enrollment_info)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "User Enrolled")

class LectureFunctionalityTest(TestCase):
    def test_ensure_post_request(self):
        client = Client()

        response = client.get('/lectures/')
        self.assertEqual(response.status_code, 400)

        response = client.get('/create-lecture/')
        self.assertEqual(response.status_code, 400)
    
    def test_get_correct_lectures(self):
        university = University(university_name="University")
        university.save()
        teacher = TeachUser(email="teacher@email.com", 
                            first_name="teacher", 
                            last_name="teacher", 
                            university=university,
                            is_teacher=True)
        teacher.save()
        unit = Unit(unit_code=1, unit_name="unit", teacher=teacher, unit_enrol_key="enrol", number_of_credits=10)
        unit.save()
        lecture_date_time = make_aware(datetime.now())
        lecture = Lecture(unit=unit, event_name="lecture", date_time=lecture_date_time)
        lecture.save()
        student = TeachUser(email="student@email.com", 
                            first_name="student", 
                            last_name="student", 
                            university=university,
                            is_teacher=False)
        student.save()
        user_enrolled_unit = UserEnrolledUnit(unit=unit, user=student)
        user_enrolled_unit.save()

        client = Client()
        user_info = {
            "email": "student@email.com",
        }

        response = client.post('/lectures/', content_type='application/json', data=user_info)

        expected_response = [{
            "unit": "unit",
            "unit_code": 1,
            "lecture_name": "lecture",
            "lecture_time": lecture_date_time.strftime("%Y-%m-%dT%H:%M:%S")
        }]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), expected_response)
    
    def test_lecture_creation(self):
        university = University(university_name="University")
        university.save()
        teacher = TeachUser(email="teacher@email.com", 
                            first_name="teacher", 
                            last_name="teacher", 
                            university=university,
                            is_teacher=True)
        teacher.save()
        unit = Unit(unit_code=1, unit_name="unit", teacher=teacher, unit_enrol_key="enrol", number_of_credits=10)
        unit.save()

        client = Client()
        lecture_info = {
            "unitCode": 1,
            "lectureName": "lecture",
            "time": datetime.now().strftime("%Y-%m-%dT%H:%M")
        }

        response = client.post('/create-lecture/', content_type='application/json', data=lecture_info)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Lecture Created Successfully")


class AssignmentFunctionalityTest(TestCase):
    def test_ensure_post_request(self):
        client = Client()

        response = client.get('/assignments/')
        self.assertEqual(response.status_code, 400)

        response = client.get('/create-assignment/')
        self.assertEqual(response.status_code, 400)

        response = client.get('/assignment-specification/')
        self.assertEqual(response.status_code, 400)

        response = client.get('/specification-name/')
        self.assertEqual(response.status_code, 400)

        response = client.get('/upload-specification/')
        self.assertEqual(response.status_code, 400)
    
    def test_get_correct_assignments(self):
        university = University(university_name="University")
        university.save()
        teacher = TeachUser(email="teacher@email.com", 
                            first_name="teacher", 
                            last_name="teacher", 
                            university=university,
                            is_teacher=True)
        teacher.save()
        unit = Unit(unit_code=1, unit_name="unit", teacher=teacher, unit_enrol_key="enrol", number_of_credits=10)
        unit.save()
        assignment_date_time = make_aware(datetime.now())
        assignment = Assignment(unit=unit, 
                                event_name="assignment", 
                                date_time=assignment_date_time,
                                weight=0.5)
        assignment.save()
        student = TeachUser(email="student@email.com", 
                            first_name="student", 
                            last_name="student", 
                            university=university,
                            is_teacher=False)
        student.save()
        user_enrolled_unit = UserEnrolledUnit(unit=unit, user=student)
        user_enrolled_unit.save()

        client = Client()
        user_info = {
            "email": "student@email.com",
        }

        response = client.post('/assignments/', content_type='application/json', data=user_info)

        expected_response = [{
            "unit": "unit",
            "unit_code": 1,
            "assignment_name": "assignment",
            "deadline": assignment_date_time.strftime("%Y-%m-%dT%H:%M:%S"),
            "weight": 0.5
        }]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), expected_response)

    def test_assignment_creation(self):
        university = University(university_name="University")
        university.save()
        teacher = TeachUser(email="teacher@email.com", 
                            first_name="teacher", 
                            last_name="teacher", 
                            university=university,
                            is_teacher=True)
        teacher.save()
        unit = Unit(unit_code=1, unit_name="unit", teacher=teacher, unit_enrol_key="enrol", number_of_credits=10)
        unit.save()

        client = Client()
        assignment_info = {
            "unitCode": 1,
            "assignmentName": "assignment",
            "deadline": datetime.now().strftime("%Y-%m-%dT%H:%M"),
            "weight": 0.5
        }

        response = client.post('/create-assignment/', content_type='application/json', data=assignment_info)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Assignment Created Successfully")


class SubmissionFunctionalityTest(TestCase):
    def test_ensure_post_request(self):
        client = Client()

        response = client.get('/submission/')
        self.assertEqual(response.status_code, 400)

        response = client.get('/submission-name/')
        self.assertEqual(response.status_code, 400)

        response = client.get('/upload-submission/')
        self.assertEqual(response.status_code, 400)

        response = client.get('/student-submissions/')
        self.assertEqual(response.status_code, 400)

        response = client.get('/student-grade/')
        self.assertEqual(response.status_code, 400)

        response = client.get('/student-feedback/')
        self.assertEqual(response.status_code, 400)
    
    def test_get_correct_submissions(self):
        university = University(university_name="University")
        university.save()
        teacher = TeachUser(email="teacher@email.com", 
                            first_name="teacher", 
                            last_name="teacher", 
                            university=university,
                            is_teacher=True)
        teacher.save()
        unit = Unit(unit_code=1, unit_name="unit", teacher=teacher, unit_enrol_key="enrol", number_of_credits=10)
        unit.save()
        assignment_date_time = make_aware(datetime.now())
        assignment = Assignment(unit=unit, 
                                event_name="assignment", 
                                date_time=assignment_date_time,
                                weight=0.5)
        assignment.save()
        student = TeachUser(email="student@email.com", 
                            first_name="student", 
                            last_name="student", 
                            university=university,
                            is_teacher=False)
        student.save()
        submission_date_time = make_aware(datetime.now())
        submission = Submission(user=student, 
                                assignment=assignment, 
                                submission_time=submission_date_time,
                                grade=70,
                                feedback="great")
        submission.save()

        client = Client()
        submission_info = {
            "unitCode": 1,
            "assignmentName": "assignment"
        }

        response = client.post('/student-submissions/', content_type='application/json', data=submission_info)

        expected_response = [{
            "user": "student@email.com",
            "submission_name": "",
            "submission_time": submission_date_time.strftime("%Y-%m-%dT%H:%M:%S"),
            "grade": 70,
            "feedback": "great"
        }]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), expected_response)
    
    def test_edit_student_grade(self):
        university = University(university_name="University")
        university.save()
        teacher = TeachUser(email="teacher@email.com", 
                            first_name="teacher", 
                            last_name="teacher", 
                            university=university,
                            is_teacher=True)
        teacher.save()
        unit = Unit(unit_code=1, unit_name="unit", teacher=teacher, unit_enrol_key="enrol", number_of_credits=10)
        unit.save()
        assignment_date_time = make_aware(datetime.now())
        assignment = Assignment(unit=unit, 
                                event_name="assignment", 
                                date_time=assignment_date_time,
                                weight=0.5)
        assignment.save()
        student = TeachUser(email="student@email.com", 
                            first_name="student", 
                            last_name="student", 
                            university=university,
                            is_teacher=False)
        student.save()
        submission_date_time = make_aware(datetime.now())
        submission = Submission(user=student, 
                                assignment=assignment, 
                                submission_time=submission_date_time,
                                grade=70,
                                feedback="great")
        submission.save()

        client = Client()
        submission_info = {
            "studentEmail": "student@email.com",
            "unitCode": 1,
            "assignmentName": "assignment",
            "grade": 80
        }

        response = client.post('/student-grade/', content_type='application/json', data=submission_info)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Grade Edit Successful")

        submission = Submission.objects.get(user=student, assignment=assignment)
        self.assertEqual(submission.grade, 80)
    
    def test_edit_student_feedback(self):
        university = University(university_name="University")
        university.save()
        teacher = TeachUser(email="teacher@email.com", 
                            first_name="teacher", 
                            last_name="teacher", 
                            university=university,
                            is_teacher=True)
        teacher.save()
        unit = Unit(unit_code=1, unit_name="unit", teacher=teacher, unit_enrol_key="enrol", number_of_credits=10)
        unit.save()
        assignment_date_time = make_aware(datetime.now())
        assignment = Assignment(unit=unit, 
                                event_name="assignment", 
                                date_time=assignment_date_time,
                                weight=0.5)
        assignment.save()
        student = TeachUser(email="student@email.com", 
                            first_name="student", 
                            last_name="student", 
                            university=university,
                            is_teacher=False)
        student.save()
        submission_date_time = make_aware(datetime.now())
        submission = Submission(user=student, 
                                assignment=assignment, 
                                submission_time=submission_date_time,
                                grade=70,
                                feedback="great")
        submission.save()

        client = Client()
        submission_info = {
            "studentEmail": "student@email.com",
            "unitCode": 1,
            "assignmentName": "assignment",
            "feedback": "amazing"
        }

        response = client.post('/student-feedback/', content_type='application/json', data=submission_info)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Feedback Edit Successful")

        submission = Submission.objects.get(user=student, assignment=assignment)
        self.assertEqual(submission.feedback, "amazing")


class QuizFunctionalityTest(TestCase):
    def test_ensure_post_request(self):
        client = Client()

        response = client.get('/quiz/')
        self.assertEqual(response.status_code, 400)

        response = client.get('/submit-answer/')
        self.assertEqual(response.status_code, 400)

        response = client.get('/quiz-results/')
        self.assertEqual(response.status_code, 400)

        response = client.get('/update-quiz/')
        self.assertEqual(response.status_code, 400)
    
    def test_get_correct_quiz(self):
        university = University(university_name="University")
        university.save()
        teacher = TeachUser(email="teacher@email.com", 
                            first_name="teacher", 
                            last_name="teacher", 
                            university=university,
                            is_teacher=True)
        teacher.save()
        unit = Unit(unit_code=1, unit_name="unit", teacher=teacher, unit_enrol_key="enrol", number_of_credits=10)
        unit.save()
        lecture_date_time = make_aware(datetime.now())
        lecture = Lecture(unit=unit, event_name="lecture", date_time=lecture_date_time)
        lecture.save()
        quiz = Quiz(lecture=lecture, total_mark=0)
        quiz.save()
        question = Question(quiz=quiz, question="question")
        question.save()
        answer = Answer(question=question, answer="answer", is_correct=True)
        answer.save()

        client = Client()
        quiz_info = {
            "unitCode": 1,
            "lectureName": "lecture"
        }

        response = client.post('/quiz/', content_type='application/json', data=quiz_info)

        expected_response = {
            "question": {"answer": True}
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), expected_response)
    
    def test_submit_user_answer(self):
        university = University(university_name="University")
        university.save()
        teacher = TeachUser(email="teacher@email.com", 
                            first_name="teacher", 
                            last_name="teacher", 
                            university=university,
                            is_teacher=True)
        teacher.save()
        unit = Unit(unit_code=1, unit_name="unit", teacher=teacher, unit_enrol_key="enrol", number_of_credits=10)
        unit.save()
        lecture_date_time = make_aware(datetime.now())
        lecture = Lecture(unit=unit, event_name="lecture", date_time=lecture_date_time)
        lecture.save()
        quiz = Quiz(lecture=lecture, total_mark=0)
        quiz.save()
        question = Question(quiz=quiz, question="question")
        question.save()
        answer = Answer(question=question, answer="answer", is_correct=True)
        answer.save()
        student = TeachUser(email="student@email.com", 
                            first_name="student", 
                            last_name="student", 
                            university=university,
                            is_teacher=False)
        student.save()

        client = Client()
        answer_info = {
            "unitCode": 1,
            "lectureName": "lecture",
            "question": "question",
            "answer": "answer",
            "userEmail": "student@email.com"
        }

        response = client.post('/submit-answer/', content_type='application/json', data=answer_info)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Answer Submitted")
    
    def test_get_quiz_results(self):
        university = University(university_name="University")
        university.save()
        teacher = TeachUser(email="teacher@email.com", 
                            first_name="teacher", 
                            last_name="teacher", 
                            university=university,
                            is_teacher=True)
        teacher.save()
        unit = Unit(unit_code=1, unit_name="unit", teacher=teacher, unit_enrol_key="enrol", number_of_credits=10)
        unit.save()
        lecture_date_time = make_aware(datetime.now())
        lecture = Lecture(unit=unit, event_name="lecture", date_time=lecture_date_time)
        lecture.save()
        quiz = Quiz(lecture=lecture, total_mark=0)
        quiz.save()
        question = Question(quiz=quiz, question="question")
        question.save()
        answer = Answer(question=question, answer="answer", is_correct=True)
        answer.save()
        student = TeachUser(email="student@email.com", 
                            first_name="student", 
                            last_name="student", 
                            university=university,
                            is_teacher=False)
        student.save()
        student_answer = UserAnswer(user=student, question=question, answer=answer)
        student_answer.save()
        user_enrolled_unit = UserEnrolledUnit(user=student, unit=unit)
        user_enrolled_unit.save()

        client = Client()
        quiz_info = {
            "unitCode": 1,
            "lectureName": "lecture"
        }

        response = client.post('/quiz-results/', content_type='application/json', data=quiz_info)

        expected_response = {
            "student@email.com": 1
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), expected_response)
    
    def test_update_quiz(self):
        university = University(university_name="University")
        university.save()
        teacher = TeachUser(email="teacher@email.com", 
                            first_name="teacher", 
                            last_name="teacher", 
                            university=university,
                            is_teacher=True)
        teacher.save()
        unit = Unit(unit_code=1, unit_name="unit", teacher=teacher, unit_enrol_key="enrol", number_of_credits=10)
        unit.save()
        lecture_date_time = make_aware(datetime.now())
        lecture = Lecture(unit=unit, event_name="lecture", date_time=lecture_date_time)
        lecture.save()
        quiz = Quiz(lecture=lecture, total_mark=0)
        quiz.save()
        question = Question(quiz=quiz, question="question")
        question.save()
        answer = Answer(question=question, answer="answer", is_correct=True)
        answer.save()

        client = Client()
        quiz_info = {
            "unitCode": 1,
            "lectureName": "lecture",
            "oldQuestion": "question",
            "newQuestion": "newQuestion",
            "newAnswers": {"newAnswers": True},
        }

        response = client.post('/update-quiz/', content_type='application/json', data=quiz_info)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Update succesful")

        new_question = Question.objects.filter(quiz=quiz)[0].question

        self.assertEqual("newQuestion", new_question)