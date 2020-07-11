from rest_framework import serializers

from teach_app_backend.models import (University, TeachUser, Unit, UserEnrolledUnit, Assignment, Submission,
                                      Lecture, Quiz, Question, Answer, UserAnswer, UserQuizPerformance)


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ('university_name', 'teacher_enrol_key', 'student_enrol_key')


class TeachUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeachUser
        fields = ('email', 'first_name', 'last_name', 'university', 'profile_picture', 'is_teacher')


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ('unit_code', 'unit_name', 'teacher', 'unit_enrol_key', 'number_of_credits')
