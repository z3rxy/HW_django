from rest_framework import viewsets, status
from django.db import transaction
from rest_framework.response import Response
from rest_framework.decorators import action
from api.models import Teacher
from api.serializers.teachers import ListTeacherSerializer, PostTeacherSerializer, PatchTeacherSerializer

class TeacherViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Teacher.objects.all()

    def get_serializer_class(self):
        if self.action == 'add_teacher': 
            return PostTeacherSerializer
        elif self.action == 'edit_teacher': 
            if self.request.method == 'PATCH':
                return PatchTeacherSerializer
            elif self.request.method == 'GET':
                return ListTeacherSerializer
        else:
            return ListTeacherSerializer
        
        return super().get_serializer_class() 

    @transaction.atomic
    @action(methods=["post"], detail=False, url_path="add-teacher")
    def add_teacher(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    @action(methods=["delete"], detail=True, url_path="remove-teacher")
    def remove_teacher(self, request, pk=None):
        try:
            teacher = Teacher.objects.get(id=pk)
        except Teacher.DoesNotExist:
            return Response({"error": "Teacher not found."}, status=status.HTTP_404_NOT_FOUND)
        
        teacher.delete()
        return Response({"message": "Teacher removed successfully."}, status=status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    @action(methods=["patch", "get"], detail=True, url_path="edit-teacher")
    def edit_teacher(self, request, pk=None):
        try:
            teacher = Teacher.objects.get(id=pk)
        except Teacher.DoesNotExist:
            return Response({"error": "Teacher not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(teacher, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)