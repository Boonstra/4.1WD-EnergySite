from django.db import models


class FlickrImage(models.Model):

    refresh_rate = models.IntegerField(default=5000, blank=False)
    tags = models.CharField(max_length=512, blank=False)

    class Meta:
        verbose_name = 'Flickr image setting'
        verbose_name_plural = 'Flickr image settings'

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(FlickrImage, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()