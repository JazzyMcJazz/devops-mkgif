from django.core.files.storage import default_storage
from django.contrib.auth.models import User
from django.db import models
import django_rq
from shutil import rmtree
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

    def remove(self):
        path = f'media/{self.pk}'
        self.delete()
        try:
            rmtree(path)
        except OSError as e:
            print("Error: %s : %s" % (path, e.strerror))


class Image(models.Model):
    def image_path(self, filename):
        return f'{self.animation.pk}/{filename}'

    animation = models.ForeignKey('Animation', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=image_path)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
