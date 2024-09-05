from rest_framework import serializers
from api.models import StudentToSubject

class ListStudentToSubjectSerializer(serializers.ModelSerializer):
    student_id = serializers.IntegerField(source='student.id')
    student = serializers.CharField(source='student.name')
    subject_id = serializers.IntegerField(source='subject.id')
    subject = serializers.CharField(source='subject.name')
    
    class Meta:
        model = StudentToSubject
        fields = ['student_id', 'student', 'subject_id', 'subject']
        
class PostStudentToSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentToSubject
        fields = ['student', 'subject']
        
class PatchStudentToSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentToSubject
        fields = ['student', 'subject']
