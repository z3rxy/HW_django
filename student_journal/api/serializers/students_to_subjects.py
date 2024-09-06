from rest_framework import serializers
from api.models import StudentToSubject

class ListStudentToSubjectSerializer(serializers.ModelSerializer):
    student_id = serializers.IntegerField(source='student.id')
    student = serializers.CharField(source='student.first_name')
    student_surname = serializers.CharField(source='student.last_name')
    subject_id = serializers.IntegerField(source='subject.id')
    subject = serializers.CharField(source='subject.name')
    
    class Meta:
        model = StudentToSubject
        fields = ['id', 'student_id', 'student', 'student_surname', 'subject_id', 'subject']
        
class PostStudentToSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentToSubject
        fields = ['student', 'subject']
        
class PatchStudentToSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentToSubject
        fields = ['student', 'subject']
