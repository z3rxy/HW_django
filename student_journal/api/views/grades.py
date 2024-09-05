from rest_framework import viewsets, status
from django.db import transaction
from rest_framework.response import Response
from rest_framework.decorators import action
from api.models import Teacher, Grade, TeacherToSubject
from api.serializers.grades import ListGradeSerializer, PostGradeSerializer, PatchGradeSerializer

class GradeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Grade.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'add_grade': 
            return PostGradeSerializer
        elif self.action == 'edit_grade': 
            if self.request.method == 'PATCH':
                return PatchGradeSerializer
            elif self.request.method == 'GET':
                return ListGradeSerializer
        else:
            return ListGradeSerializer
        
        return super().get_serializer_class()

    @transaction.atomic
    @action(methods=['post'], detail=False, url_path='add-grade')
    def add_grade(self, request):
        serializer = self.get_serializer_class(data=request.data)
        
        if serializer.is_valid():
            teacher_id = request.data.get('author')
            subject_id = request.data.get('subject')
            try:
                teacher = Teacher.objects.get(id=teacher_id)
            except Teacher.DoesNotExist:
                return Response({"error": "Teacher not found."}, status=status.HTTP_404_NOT_FOUND)

            if not TeacherToSubject.objects.filter(teacher=teacher, subject_id=subject_id).exists():
                return Response({"error": "You can only grade subjects you teach."}, status=status.HTTP_403_FORBIDDEN)
            serializer.save(author=teacher)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    @action(methods=["delete"], detail=True, url_path="remove-grade")
    def remove_grade(self, request, pk=None):
        try:
            grade = Grade.objects.get(id=pk)
        except Grade.DoesNotExist:
            return Response({"error": "Grade not found."}, status=status.HTTP_404_NOT_FOUND)
        
        grade.delete()
        return Response({"message": "Grade removed successfully."}, status=status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    @action(methods=["patch"], detail=True, url_path="edit-grade")
    def edit_grade(self, request, pk=None):
        try:
            grade = Grade.objects.get(id=pk)
        except Grade.DoesNotExist:
            return Response({"error": "Grade not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer_class(grade, data=request.data, partial=True)
        if serializer.is_valid():
            teacher = request.user
            subject_id = serializer.validated_data.get('subject')

            if subject_id and not TeacherToSubject.objects.filter(teacher=teacher, subject_id=subject_id).exists():
                return Response({"error": "You can only grade subjects you teach."}, status=status.HTTP_403_FORBIDDEN)
            
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)