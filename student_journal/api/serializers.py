from rest_framework import serializers
from .models import Student, Teacher, Subject, Comment, Grade, StudentToSubject, TeacherToSubject

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'

class StudentToSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentToSubject
        fields = '__all__'

class TeacherToSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherToSubject
        fields = '__all__'
