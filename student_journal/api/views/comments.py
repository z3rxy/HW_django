from rest_framework import viewsets, status
from django.db import transaction
from rest_framework.response import Response
from rest_framework.decorators import action
from api.models import Comment
from api.serializers.comments import ListCommentSerializer, PostCommentSerializer, PatchCommentSerializer

class CommentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Comment.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'add_teacher': 
            return PostCommentSerializer
        elif self.action == 'edit_teacher': 
            if self.request.method == 'PATCH':
                return PatchCommentSerializer
            elif self.request.method == 'GET':
                return ListCommentSerializer
        else:
            return ListCommentSerializer
        
        return super().get_serializer_class() 

    @transaction.atomic
    @action(methods=["post"], detail=False, url_path="add-comment")
    def add_comment(self, request):
        serializer = self.get_serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    @action(methods=["delete"], detail=True, url_path="remove-comment")
    def remove_comment(self, request, pk=None):
        try:
            comment = Comment.objects.get(id=pk)
        except Comment.DoesNotExist:
            return Response({"error": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)
        
        comment.delete()
        return Response({"message": "Comment removed successfully."}, status=status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    @action(methods=["patch"], detail=True, url_path="edit-comment")
    def edit_comment(self, request, pk=None):
        try:
            comment = Comment.objects.get(id=pk)
        except Comment.DoesNotExist:
            return Response({"error": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer_class(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)