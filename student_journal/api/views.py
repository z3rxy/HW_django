from rest_framework import viewsets, status
from django.db import transaction
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Student, Teacher, Subject, Comment, Grade, StudentToSubject, TeacherToSubject
from .serializers import *

class StudentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    @transaction.atomic
    @action(methods=["post"], detail=False, url_path="add-student")
    def add_student(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    @action(methods=["delete"], detail=True, url_path="remove-student")
    def remove_student(self, request, pk=None):
        try:
            student = Student.objects.get(id=pk)
        except Student.DoesNotExist:
            return Response({"error": "Student not found."}, status=status.HTTP_404_NOT_FOUND)
        
        student.delete()
        return Response({"message": "Student removed successfully."}, status=status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    @action(methods=["patch"], detail=True, url_path="edit-student")
    def edit_student(self, request, pk=None):
        try:
            student = Student.objects.get(id=pk)
        except Student.DoesNotExist:
            return Response({"error": "Student not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeacherViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    @transaction.atomic
    @action(methods=["post"], detail=False, url_path="add-teacher")
    def add_teacher(self, request):
        serializer = self.serializer_class(data=request.data)
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
    @action(methods=["patch"], detail=True, url_path="edit-teacher")
    def edit_teacher(self, request, pk=None):
        try:
            teacher = Teacher.objects.get(id=pk)
        except Teacher.DoesNotExist:
            return Response({"error": "Teacher not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(teacher, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    @transaction.atomic
    @action(methods=["post"], detail=False, url_path="add-subject")
    def add_subject(self, request):
        serializer = self.serializer_class(data=request.data)
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
        
        serializer = self.serializer_class(subject, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    @transaction.atomic
    @action(methods=["post"], detail=False, url_path="add-comment")
    def add_comment(self, request):
        serializer = self.serializer_class(data=request.data)
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
        
        serializer = self.serializer_class(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GradeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

    @transaction.atomic
    @action(methods=['post'], detail=False, url_path='add-grade')
    def add_grade(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            teacher_id = request.data.get('author')
            subject_id = request.data.get('subject')
            try:
                teacher = Teacher.objects.get(id=teacher_id)
            except Teacher.DoesNotExist:
                return Response({"error": "Teacher not found."}, status=status.HTTP_404_NOT_FOUND)

            if not TeacherToSubject.objects.filter(teacher=teacher, subject_id=subject_id).exists():
                return Response({"error": "You can only grade subjects you teach."}, status=status.HTTP_403_FORBIDDEN)
            print('yayayayyayDSPKCWPEOFC', TeacherToSubject.objects.filter(teacher=teacher, subject_id=subject_id))
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
        
        serializer = self.serializer_class(grade, data=request.data, partial=True)
        if serializer.is_valid():
            teacher = request.user
            subject_id = serializer.validated_data.get('subject')

            if subject_id and not TeacherToSubject.objects.filter(teacher=teacher, subject_id=subject_id).exists():
                return Response({"error": "You can only grade subjects you teach."}, status=status.HTTP_403_FORBIDDEN)
            
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentToSubjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StudentToSubject.objects.all()
    serializer_class = StudentToSubjectSerializer

class TeacherToSubjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TeacherToSubject.objects.all()
    serializer_class = TeacherToSubjectSerializer
