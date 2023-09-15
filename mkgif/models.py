from django.db import models
from django.contrib.auth.models import User
import django_rq
from .utils import mk_gif_ffmpeg

class Animation(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def enqueue(self, params):
        django_rq.enqueue(mk_gif_ffmpeg, {
            'pk': self.pk,
            'params': params,
            }
        )


class Image(models.Model):
    def image_path(self, filename):
        return f'{self.animation.pk}/{filename}'

    animation = models.ForeignKey('Animation', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=image_path)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
