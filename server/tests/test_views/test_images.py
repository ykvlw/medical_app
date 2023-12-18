import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from medical_project.models import Annotation, ImageFile
from medical_project.serializers import GetImageSerializer
from tests.base import PathHelper
from tests.base.base import api_client_with_credentials
from tests.factories import ImageFileFactory


@pytest.mark.django_db
class TestImageFileViewSet:
    @classmethod
    def setup_class(cls) -> None:
        cls.url = reverse("images-list")
        cls.file_path = PathHelper.relative_path("tests/files/test_image.jpg")

    def test_get_images(self, api_client_with_credentials: APIClient) -> None:
        client = api_client_with_credentials
        images = ImageFileFactory.create_batch(3)
        expected_data = GetImageSerializer(images, many=True).data
        for expected_data_item in expected_data:
            expected_data_item["image"] = "http://testserver" + expected_data_item["image"]

        response = client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data

    def test_retrieve_image_file(self, api_client_with_credentials: APIClient) -> None:
        client = api_client_with_credentials
        image_file = ImageFileFactory.create()
        expected_data = GetImageSerializer(image_file).data
        expected_data["image"] = "http://testserver" + expected_data["image"]

        response = client.get(reverse("images-detail", args=[image_file.id]))
        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data

    def test_create_image_file_with_annotation(
        self, api_client_with_credentials: APIClient
    ) -> None:
        client = api_client_with_credentials
        with open(self.file_path, "rb") as file:
            file_data = file.read()
        uploaded_file = SimpleUploadedFile("test_image.jpg", file_data, content_type="image/jpeg")

        data = {
            "image": uploaded_file,
            "annotation.class_id": "teeth",
            "annotation.surface": ["B,O,L"],
        }

        response = client.post(self.url, data, format="multipart")
        assert response.status_code == status.HTTP_201_CREATED
        assert ImageFile.objects.count() == 1
        assert Annotation.objects.count() == 1

        image_file = ImageFile.objects.first()
        annotation = Annotation.objects.first()
        assert image_file.id == annotation.image_file.id
        assert annotation.class_id == "teeth"
        assert annotation.surface == ["B,O,L"]

    def test_create_image_file_without_annotation(
        self, api_client_with_credentials: APIClient
    ) -> None:
        client = api_client_with_credentials
        with open(self.file_path, "rb") as file:
            file_data = file.read()
        uploaded_file = SimpleUploadedFile("test_image.jpg", file_data, content_type="image/jpeg")

        data = {
            "image": uploaded_file,
        }

        response = client.post(self.url, data, format="multipart")
        assert response.status_code == status.HTTP_201_CREATED
        assert ImageFile.objects.count() == 1
        assert Annotation.objects.count() == 0

    def test_create_without_image(self, api_client_with_credentials: APIClient) -> None:
        client = api_client_with_credentials
        data = {
            "annotation": "your_image_file_data_here",
        }

        response = client.post(self.url, data, format="multipart")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
