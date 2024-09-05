from rest_framework import viewsets, status
from django.db import transaction
from rest_framework.response import Response
from rest_framework.decorators import action
from api.models import TeacherToSubject
from api.serializers.teachers_to_subjects import ListTeacherToSubjectSerializer, PostTeacherToSubjectSerializer, PatchTeacherToSubjectSerializer

class TeacherToSubjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TeacherToSubject.objects.all()

    def get_serializer_class(self):
        if self.action == 'add_teacher_to_subject': 
            return PostTeacherToSubjectSerializer
        elif self.action == 'edit_teacher_to_subject': 
            if self.request.method == 'PATCH':
                return PatchTeacherToSubjectSerializer
            elif self.request.method == 'GET':
                return ListTeacherToSubjectSerializer
        else:
            return ListTeacherToSubjectSerializer
        
        return super().get_serializer_class()

    @transaction.atomic
    @action(methods=["post"], detail=False, url_path="add-teacher-to-subject")
    def add_teacher_to_subject(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    @action(methods=["delete", "get"], detail=True, url_path="remove-teacher-to-subject")
    def remove_teacher_to_subject(self, request, pk=None):
        try:
            teacher_to_subject = TeacherToSubject.objects.get(id=pk)
        except TeacherToSubject.DoesNotExist:
            return Response({"error": "Teacher to subject relation not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if request.method == 'GET':
            serializer = self.get_serializer(teacher_to_subject)
            return Response(serializer.data)
        else:
            teacher_to_subject.delete()
            return Response({"message": "Teacher to subject relation removed successfully."}, status=status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    @action(methods=["patch", "get"], detail=True, url_path="edit-teacher-to-subject")
    def edit_teacher_to_subject(self, request, pk=None):
        try:
            teacher_to_subject = TeacherToSubject.objects.get(id=pk)
        except TeacherToSubject.DoesNotExist:
            return Response({"error": "Teacher to subject relation not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = self.get_serializer(teacher_to_subject)
            return Response(serializer.data)

        elif request.method == 'PATCH':
            serializer = self.get_serializer(teacher_to_subject, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
