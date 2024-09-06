from rest_framework import serializers
from api.models import TeacherToSubject

class ListTeacherToSubjectSerializer(serializers.ModelSerializer):
    teacher_id = serializers.IntegerField(source='teacher.id')
    teacher = serializers.CharField(source='teacher.first_name')
    teacher_surname = serializers.CharField(source='teacher.last_name')
    subject_id = serializers.IntegerField(source='subject.id')
    subject = serializers.CharField(source='subject.name')
    
    class Meta:
        model = TeacherToSubject
        fields = ['id', 'teacher_id', 'teacher', 'teacher_surname', 'subject_id', 'subject']
        
class PostTeacherToSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherToSubject
        fields = ['teacher', 'subject']
        
class PatchTeacherToSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherToSubject
        fields = ['teacher', 'subject']