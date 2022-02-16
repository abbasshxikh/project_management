from django.db import models
from accounts.constants import FileTypeConstants
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class FileType(models.Model):
    name = models.CharField(max_length=20, choices=FileTypeConstants.get_choices(), default=FileTypeConstants.DOCUMENT.value)

    @classmethod
    def get_file_by_name(cls, name):
        return FileType.objects.get(name='Document')


class FileStorage(models.Model):
    
    file = models.FileField(upload_to="files/%Y/%m/%d")
    file_type = models.ForeignKey(FileType, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return str(self.file)
