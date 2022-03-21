from django.db import models
from model_utils.models import TimeStampedModel


class UploadedFile(TimeStampedModel):
    def upload_path(self, name):
        return 'file-uploads/' + self.name + '/' + name

    file = models.FileField(
        upload_to=upload_path,
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
