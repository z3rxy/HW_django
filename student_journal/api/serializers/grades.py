from rest_framework import serializers
from api.models import Grade

class ListGradeSerializer(serializers.ModelSerializer):
    student = serializers.CharField(source="student.first_name")
    student_surname = serializers.CharField(source="student.last_name")
    author = serializers.CharField(source="author.first_name")
    author_surname = serializers.CharField(source="author.last_name")
    subject = serializers.CharField(source="subject.name")
    class Meta:
        model = Grade
        fields = ['id', 'subject', 'grade', 'student', 'student_surname', 'author', 'author_surname']
        
class PostGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['subject', 'grade', 'student', 'author']
        
class PatchGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['subject', 'grade']