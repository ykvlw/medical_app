from django.db import models

from .base import BaseModel


class ImageFile(BaseModel):
    image = models.ImageField(upload_to="entity_images/")
