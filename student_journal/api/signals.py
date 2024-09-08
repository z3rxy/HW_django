from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import StudentToSubject, Grade

@receiver(post_delete, sender=StudentToSubject)
def remove_grades_on_subject_removal(sender, instance, **kwargs):
    student = instance.student
    subject = instance.subject
    Grade.objects.filter(student=student, subject=subject).delete()
