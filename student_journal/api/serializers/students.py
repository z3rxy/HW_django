from rest_framework import serializers
from api.models import Student

class ListStudentSerializer(serializers.ModelSerializer):
    subjects = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'date_of_birth', 'group', 'subjects']
        
        
class PostStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'date_of_birth', 'group']
      
        
class PatchStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'date_of_birth', 'group']