from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Student, Grade

@receiver(m2m_changed, sender=Student.subjects.through)
def remove_grades_on_subject_removal(sender, instance, action, reverse, pk_set, **kwargs):
    if action == 'post_remove':
        for subject_id in pk_set:
            Grade.objects.filter(student=instance, subject_id=subject_id).delete()
