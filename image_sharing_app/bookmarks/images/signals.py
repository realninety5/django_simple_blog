from django.dispatch import receiver
from .models import Image
from django.db.models.signals import m2m_changed

# A signal to change the number of likes an image gets once in a while rather than immediately---> apps.py loads
@receiver(m2m_changed, sender=Image.user_like.through)
def users_like_changed(sender, instance, **kwargs):
    instance.total_likes = instance.user_like.count()
    instance.save()
