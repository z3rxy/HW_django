from rest_framework import viewsets, status
from django.db import transaction
from rest_framework.response import Response
from rest_framework.decorators import action
from api.models import Comment, Student, Teacher
from api.serializers.comments import ListCommentSerializer, PostCommentSerializer, PatchCommentSerializer
from api.serializers.students import ListStudentSerializer
from api.serializers.teachers import ListTeacherSerializer

class CommentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Comment.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'add_comment': 
            return PostCommentSerializer
        elif self.action == 'edit_comment': 
            if self.request.method == 'PATCH':
                return PatchCommentSerializer
            elif self.request.method == 'GET':
                return ListCommentSerializer
        elif self.action == 'add_comment:':
            return PostCommentSerializer
        else:
            return ListCommentSerializer
        
        return super().get_serializer_class() 

    @transaction.atomic
    @action(methods=["post", "get"], detail=False, url_path="add-comment")
    def add_comment(self, request):
        
        if request.method == "GET":
            students = Student.objects.all()
            teachers = Teacher.objects.all()

            student_serializer = ListStudentSerializer(students, many=True)
            teacher_serializer = ListTeacherSerializer(teachers, many=True)

            return Response({
                "students": student_serializer.data,
                "teachers": teacher_serializer.data
            }, status=status.HTTP_200_OK)
        else:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    @action(methods=["delete", "get"], detail=True, url_path="remove-comment")
    def remove_comment(self, request, pk=None):
        try:
            comment = Comment.objects.get(id=pk)
        except Comment.DoesNotExist:
            return Response({"error": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if request.method == 'GET':
            serializer = self.get_serializer(comment)
            return Response(serializer.data)
        else:
            comment.delete()
            return Response({"message": "Comment removed successfully."}, status=status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    @action(methods=["patch", "get"], detail=True, url_path="edit-comment")
    def edit_comment(self, request, pk=None):
        try:
            comment = Comment.objects.get(id=pk)
        except Comment.DoesNotExist:
            return Response({"error": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if request.method == 'GET':
            serializer = self.get_serializer(comment)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = self.get_serializer(comment, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)