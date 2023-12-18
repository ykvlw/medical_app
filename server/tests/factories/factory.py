import factory
from factory.django import DjangoModelFactory

from medical_project.models import Annotation, ImageFile, Tags


class TagsFactory(DjangoModelFactory):
    class Meta:
        model = Tags

    tag = factory.Faker("random_int", min=1, max=100)  # You can customize this as needed


class ImageFileFactory(DjangoModelFactory):
    class Meta:
        model = ImageFile

    image = factory.django.ImageField(filename="test_image.jpg", width=100, height=100)


class AnnotationFactory(DjangoModelFactory):
    class Meta:
        model = Annotation

    class_id = factory.Faker("word")
    surface = factory.Faker("words", nb=3)
    type = factory.Faker("word")
    start_x = factory.Faker("random_int", min=0, max=1000)
    start_y = factory.Faker("random_int", min=0, max=1000)
    end_x = factory.Faker("random_int", min=0, max=1000)
    end_y = factory.Faker("random_int", min=0, max=1000)
    confirmed = factory.Faker("boolean")
    confidence_percent = factory.Faker("pydecimal", left_digits=3, right_digits=2, positive=True)
    image_file = factory.SubFactory(ImageFileFactory)
    parent = None
