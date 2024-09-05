from rest_framework import viewsets, status
from django.db import transaction
from rest_framework.response import Response
from rest_framework.decorators import action
from api.models import Subject
from api.serializers.subjects import ListSubjectSerializer, PostSubjectSerializer, PatchSubjectSerializer

class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Subject.objects.all()

    def get_serializer_class(self):
        if self.action == 'add_teacher': 
            return PostSubjectSerializer
        elif self.action == 'edit_teacher': 
            if self.request.method == 'PATCH':
                return PatchSubjectSerializer
            elif self.request.method == 'GET':
                return ListSubjectSerializer
        else:
            return ListSubjectSerializer
        
        return super().get_serializer_class() 

    @transaction.atomic
    @action(methods=["post"], detail=False, url_path="add-subject")
    def add_subject(self, request):
        serializer = self.get_serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    @action(methods=["delete"], detail=True, url_path="remove-subject")
    def remove_subject(self, request, pk=None):
        try:
            subject = Subject.objects.get(id=pk)
        except Subject.DoesNotExist:
            return Response({"error": "Subject not found."}, status=status.HTTP_404_NOT_FOUND)
        
        subject.delete()
        return Response({"message": "Subject removed successfully."}, status=status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    @action(methods=["patch"], detail=True, url_path="edit-subject")
    def edit_subject(self, request, pk=None):
        try:
            subject = Subject.objects.get(id=pk)
        except Subject.DoesNotExist:
            return Response({"error": "Subject not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer_class(subject, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)