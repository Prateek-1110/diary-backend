from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.diary.models import DiaryEntry
from apps.letters.models import FutureLetter
from .models import TimelineEvent

@receiver(post_save, sender=DiaryEntry)
def create_timeline_from_diary(sender, instance, created, **kwargs):
    if created:
        TimelineEvent.objects.create(
            user=instance.user,
            label=instance.title or "Diary Entry",
            source='diary',
            source_id=instance.id,
            event_date=instance.written_at.date(),
            is_milestone=False,
        )

@receiver(post_save, sender=FutureLetter)
def create_timeline_from_letter(sender, instance, created, **kwargs):
    if created:
        TimelineEvent.objects.create(
            user=instance.user,
            label=instance.subject or "Future Letter",
            source='letter',
            source_id=instance.id,
            event_date=instance.unlocks_at.date(),
            is_milestone=False,
        )