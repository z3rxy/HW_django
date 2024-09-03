from django.db import models


class TimeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Person(TimeModel):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()

    class Meta:
        abstract = True


class Student(Person):
    group = models.CharField(max_length=10)
    
    subjects = models.ManyToManyField(
        'Subject', 
        through='StudentToSubject', 
        related_name='students',
        related_query_name='student'
    )

    class Meta:
        db_table = 'students'
        verbose_name = 'Student'
        verbose_name_plural = 'Students'


class Teacher(Person):
    department = models.CharField(max_length=50, null=True, blank=True)

    subjects = models.ManyToManyField(
        'Subject', 
        through='TeacherToSubject', 
        related_name='teachers',
        related_query_name='teacher'
    )

    class Meta:
        db_table = 'teachers'
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'


class Subject(TimeModel):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'subjects'
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'


class StudentToSubject(models.Model):
    student = models.ForeignKey(
        Student, 
        related_name="student_subjects", 
        on_delete=models.CASCADE
    )
    subject = models.ForeignKey(
        Subject, 
        related_name="subject_students", 
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'student_to_subjects'
        verbose_name = 'Student-Subject Relation'
        verbose_name_plural = 'Student-Subject Relations'
        unique_together = ('student', 'subject')


class TeacherToSubject(models.Model):
    teacher = models.ForeignKey(
        Teacher, 
        related_name="teacher_subjects", 
        on_delete=models.CASCADE
    )
    subject = models.ForeignKey(
        Subject, 
        related_name="subject_teachers", 
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'teacher_to_subjects'
        verbose_name = 'Teacher-Subject Relation'
        verbose_name_plural = 'Teacher-Subject Relations'
        unique_together = ('teacher', 'subject')


class Comment(TimeModel):
    student = models.ForeignKey(
        Student, 
        related_name="comments", 
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        Teacher, 
        related_name="comments", 
        on_delete=models.CASCADE
    )
    text = models.TextField()

    class Meta:
        db_table = 'comments'
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'


class Grade(TimeModel):
    student = models.ForeignKey(
        Student, 
        related_name="grades", 
        on_delete=models.CASCADE
    )
    subject = models.ForeignKey(
        Subject, 
        related_name='grades',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        Teacher, 
        related_name="given_grades", 
        on_delete=models.CASCADE
    )
    grade = models.PositiveIntegerField()

    class Meta:
        db_table = 'grades'
        verbose_name = 'Grade'
        verbose_name_plural = 'Grades'
