from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('students', StudentViewSet, basename='students')
router.register('teachers', TeacherViewSet, basename='teachers')
router.register('subjects', SubjectViewSet, basename='subjects')
router.register('comments', CommentViewSet, basename='comments')
router.register('grades', GradeViewSet, basename='grades')
router.register('student-to-subjects', StudentToSubjectViewSet, basename='student-to-subjects')
router.register('teacher-to-subjects', TeacherToSubjectViewSet, basename='teacher-to-subjects')

urlpatterns = [
    path('', include(router.urls)),
]
