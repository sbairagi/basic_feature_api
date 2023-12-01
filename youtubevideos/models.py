from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from fcm_django.models import FCMDevice

# Create your models here.

class YouubeVideos(models.Model):
    videoid = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    desc = models.TextField(default="")

    def __str__(self):
        return self.desc

@receiver(post_save, sender=YouubeVideos, dispatch_uid="knowledge_push_notification")
def post_save_youtube_video_receiver(sender, instance, *args, **kwargs):
    devices = FCMDevice.objects.all()
    devices.send_message(
        title="New Video ({})".format(instance.title),
        body="{}".format(instance.desc),
        color="#ffa813",
        data={"type": "youtube video", "description": instance.desc}
    )