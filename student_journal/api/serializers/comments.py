from rest_framework import serializers
from api.models import Comment

class ListCommentSerializer(serializers.ModelSerializer):
    student = serializers.CharField(source="student.first_name")
    student_surname = serializers.CharField(source="student.last_name")
    author = serializers.CharField(source="author.first_name")
    author_surname = serializers.CharField(source="author.last_name")

    class Meta:
        model = Comment
        fields = ['id', 'student', 'student_surname', 'text', 'author', 'author_surname']
        
class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['student', 'text', 'author']
        
class PatchCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['student', 'text']