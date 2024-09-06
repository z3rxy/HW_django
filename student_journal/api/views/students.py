from rest_framework import viewsets, status
from django.db import transaction
from rest_framework.response import Response
from rest_framework.decorators import action
from api.models import Student
from api.serializers.students import ListStudentSerializer, PostStudentSerializer, PatchStudentSerializer

class StudentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Student.objects.all()

    def get_serializer_class(self):
        if self.action == 'add_student': 
            return PostStudentSerializer
        elif self.action == 'edit_student': 
            if self.request.method == 'PATCH':
                return PatchStudentSerializer
            elif self.request.method == 'GET':
                return ListStudentSerializer
        else:
            return ListStudentSerializer
        
        return super().get_serializer_class() 

    @transaction.atomic
    @action(methods=["post", "get"], detail=False, url_path="add-student")
    def add_student(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    @action(methods=["delete", "get"], detail=True, url_path="remove-student")
    def remove_student(self, request, pk=None):
        try:
            student = Student.objects.get(id=pk)
        except Student.DoesNotExist:
            return Response({"error": "Student not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if request.method == 'GET':
            serializer = self.get_serializer(student)
            return Response(serializer.data)
        else:
            student.delete()
            return Response({"message": "Student removed successfully."}, status=status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    @action(methods=["patch", "get"], detail=True, url_path="edit-student")
    def edit_student(self, request, pk=None):
        try:
            student = Student.objects.get(id=pk)
        except Student.DoesNotExist:
            return Response({"error": "Student not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = self.get_serializer(student)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = self.get_serializer(student, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)