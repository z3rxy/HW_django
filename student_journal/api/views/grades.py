from rest_framework import viewsets, status
from django.db import transaction
from rest_framework.response import Response
from rest_framework.decorators import action
from api.models import Teacher, Grade, TeacherToSubject, Student
from api.serializers.grades import ListGradeSerializer, PostGradeSerializer, PatchGradeSerializer
from api.serializers.students import ListStudentSerializer
from api.serializers.teachers import ListTeacherSerializer

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
    @action(methods=['post', "get"], detail=False, url_path='add-grade')
    def add_grade(self, request):
        
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
                teacher_id = request.data.get('author')
                subject_id = request.data.get('subject')
                student_id = request.data.get('student')
                try:
                    teacher = Teacher.objects.get(id=teacher_id)
                except Teacher.DoesNotExist:
                    return Response({"error": "Teacher not found."}, status=status.HTTP_404_NOT_FOUND)
                
                try:
                    student = Student.objects.get(id=student_id)
                except Student.DoesNotExist:
                    return Response({"error": "Student not found."}, status=status.HTTP_404_NOT_FOUND)

                if not TeacherToSubject.objects.filter(teacher=teacher, subject_id=subject_id).exists():
                    return Response({"error": "You can only grade subjects you teach."}, status=status.HTTP_403_FORBIDDEN)
                
                if not student.subjects.filter(id=subject_id).exists():
                    return Response({"error": "The student is not enrolled in this subject."}, status=status.HTTP_403_FORBIDDEN)
                
                serializer.save(author=teacher)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    @action(methods=["delete", "get"], detail=True, url_path="remove-grade")
    def remove_grade(self, request, pk=None):
        try:
            grade = Grade.objects.get(id=pk)
        except Grade.DoesNotExist:
            return Response({"error": "Grade not found."}, status=status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
            serializer = self.get_serializer(grade)
            return Response(serializer.data)
        else:
            grade.delete()
            return Response({"message": "Grade removed successfully."}, status=status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    @action(methods=["patch", "get"], detail=True, url_path="edit-grade")
    def edit_grade(self, request, pk=None):
        try:
            grade = Grade.objects.get(id=pk)
        except Grade.DoesNotExist:
            return Response({"error": "Grade not found."}, status=status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
            serializer = self.get_serializer(grade)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = self.get_serializer(grade, data=request.data, partial=True)
            if serializer.is_valid():
                teacher = request.user
                subject_id = serializer.validated_data.get('subject')

                if subject_id and not TeacherToSubject.objects.filter(teacher=teacher, subject_id=subject_id).exists():
                    return Response({"error": "You can only grade subjects you teach."}, status=status.HTTP_403_FORBIDDEN)

                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)