import random

from django.contrib.auth import get_user_model
from django.db import migrations
from faker import Faker


def generate_fake_data(apps, schema_editor):
    Faker.seed(1234)
    faker = Faker()

    Tags = apps.get_model("medical_project", "Tags")
    ImageFile = apps.get_model("medical_project", "ImageFile")
    Annotation = apps.get_model("medical_project", "Annotation")

    num_records = 100

    User = get_user_model()

    user, created = User.objects.get_or_create(username="admin_user")
    if created:
        user.set_password("strong_password")
        user.is_staff = True
        user.save()

    annotations = []
    tags = [Tags.objects.create(tag=faker.random_int(min=0, max=1000)) for _ in range(10)]

    for _ in range(num_records):
        parent = random.choice(annotations + [None])

        if parent:
            image_file = parent.image_file
        else:
            image_file = ImageFile.objects.create(image="path/to/fake/image.jpg")

        annotation = Annotation.objects.create(
            class_id=faker.word(),
            surface=[faker.word() for _ in range(3)],
            type=faker.word(),
            start_x=faker.random_int(min=0, max=100),
            start_y=faker.random_int(min=0, max=100),
            end_x=faker.random_int(min=0, max=100),
            end_y=faker.random_int(min=0, max=100),
            confirmed=faker.boolean(),
            confidence_percent=faker.pydecimal(left_digits=2, right_digits=2, positive=True),
            image_file=image_file,
            parent=parent,
        )

        for _ in range(random.randint(0, 3)):
            annotation.tags.add(random.choice(tags))

        annotations.append(annotation)


class Migration(migrations.Migration):
    dependencies = [
        ("medical_project", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(generate_fake_data),
    ]
