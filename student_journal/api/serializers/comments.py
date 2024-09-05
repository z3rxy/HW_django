from rest_framework import serializers
from api.models import Comment

class ListCommentSerializer(serializers.ModelSerializer):
    student = serializers.CharField(source="student.name")
    author = serializers.CharField(source="author.name")

    class Meta:
        model = Comment
        fields = ['id', 'student', 'text', 'author']
        
class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['student', 'text', 'author']
        
class PatchCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['student', 'text']