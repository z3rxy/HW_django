from rest_framework import viewsets, status
from django.db import transaction
from rest_framework.response import Response
from rest_framework.decorators import action
from api.models import StudentToSubject
from api.serializers.students_to_subjects import (
    ListStudentToSubjectSerializer,
    PostStudentToSubjectSerializer,
    PatchStudentToSubjectSerializer
)

class StudentToSubjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StudentToSubject.objects.all()

    def get_serializer_class(self):
        if self.action == 'add_student_to_subject': 
            return PostStudentToSubjectSerializer
        elif self.action == 'edit_student_to_subject': 
            if self.request.method == 'PATCH':
                return PatchStudentToSubjectSerializer
            elif self.request.method == 'GET':
                return ListStudentToSubjectSerializer
        else:
            return ListStudentToSubjectSerializer

    @transaction.atomic
    @action(methods=["post"], detail=False, url_path="add-student-to-subject")
    def add_student_to_subject(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    @action(methods=["delete", "get"], detail=True, url_path="remove-student-to-subject")
    def remove_student_to_subject(self, request, pk=None):
        try:
            student_to_subject = StudentToSubject.objects.get(id=pk)
        except StudentToSubject.DoesNotExist:
            return Response({"error": "Student to subject relation not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if request.method == 'GET':
            serializer = self.get_serializer(student_to_subject)
            return Response(serializer.data)
        else:
            student_to_subject.delete()
            return Response({"message": "Student to subject relation removed successfully."}, status=status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    @action(methods=["patch", "get"], detail=True, url_path="edit-student-to-subject")
    def edit_student_to_subject(self, request, pk=None):
        try:
            student_to_subject = StudentToSubject.objects.get(id=pk)
        except StudentToSubject.DoesNotExist:
            return Response({"error": "Student to subject relation not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = self.get_serializer(student_to_subject)
            return Response(serializer.data)

        elif request.method == 'PATCH':
            serializer = self.get_serializer(student_to_subject, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
