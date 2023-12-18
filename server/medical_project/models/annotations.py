import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models

from .base import BaseModel
from .images import ImageFile


class Tags(BaseModel):
    tag = models.CharField(max_length=50)


class Annotation(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    class_id = models.CharField(max_length=100, null=True)
    surface = ArrayField(models.CharField(max_length=50), blank=True, default=list)
    type = models.CharField(max_length=50, null=True)
    start_x = models.IntegerField(null=True)
    start_y = models.IntegerField(null=True)
    end_x = models.IntegerField(null=True)
    end_y = models.IntegerField(null=True)
    confirmed = models.BooleanField(null=True)
    confidence_percent = models.DecimalField(null=True, decimal_places=2, max_digits=5)
    image_file = models.ForeignKey(
        ImageFile, related_name="annotation", on_delete=models.CASCADE, null=True
    )
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    tags = models.ManyToManyField(Tags, related_name="annotations", blank=True)
