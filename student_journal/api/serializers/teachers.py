from rest_framework import serializers
from api.models import Teacher

class ListTeacherSerializer(serializers.ModelSerializer):
    subjects = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'last_name', 'date_of_birth', 'department', 'subjects']
        
        
class PostTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'date_of_birth', 'department']
      
        
class PatchTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'date_of_birth', 'department']
