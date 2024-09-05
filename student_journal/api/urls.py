from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views.teachers import TeacherViewSet
from api.views.students import StudentViewSet
from api.views.subjects import SubjectViewSet
from api.views.comments import CommentViewSet
from api.views.grades import GradeViewSet
from api.views.students_to_subjects import StudentToSubjectViewSet
from api.views.teachers_to_subjects import TeacherToSubjectViewSet

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
