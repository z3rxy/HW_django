from rest_framework import serializers
from api.models import Grade

class ListGradeSerializer(serializers.ModelSerializer):
    student = serializers.CharField(source="student.name")
    teacher = serializers.CharField(source="teacher.name")
    subject = serializers.CharField(source="subject.name")
    class Meta:
        model = Grade
        fields = ['id', 'subject', 'grade', 'student', 'teacher']
        
class PostGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['subject', 'grade', 'student', 'teacher']
        
class PatchGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['subject', 'grade']