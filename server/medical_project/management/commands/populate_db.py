import random

from django.core.management.base import BaseCommand
from faker import Faker

from medical_project.models import Annotation, ImageFile, Tags


class Command(BaseCommand):
    help = "Populate the database with fake data"

    def add_arguments(self, parser):
        parser.add_argument("num", type=int, help="Indicates the number of records to be created")

    def handle(self, *args: any, **options: any) -> None:
        faker = Faker()
        num_records = options["num"]

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

        self.stdout.write(
            self.style.SUCCESS(f"Successfully populated database with {num_records} records")
        )
