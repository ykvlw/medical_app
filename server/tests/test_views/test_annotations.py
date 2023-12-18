import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from tests.base.base import api_client_with_credentials
from tests.factories import AnnotationFactory, ImageFileFactory


@pytest.mark.django_db(transaction=True)
class TestAnnotationUpdateViewSet:
    @classmethod
    def setup_class(cls) -> None:
        cls.detail_url_name = "annotations-detail"

    def test_update_annotation(self, api_client_with_credentials: APIClient) -> None:
        client = api_client_with_credentials
        annotation = AnnotationFactory.create()
        update_data = {"class_id": "updated_class"}
        detail_url = reverse(self.detail_url_name, kwargs={"pk": annotation.id})

        response = client.patch(detail_url, update_data)
        assert response.status_code == 200
        annotation.refresh_from_db()
        assert annotation.class_id == "updated_class"

    def test_update_annotation_with_wrong_data(
        self, api_client_with_credentials: APIClient
    ) -> None:
        client = api_client_with_credentials
        annotation = AnnotationFactory.create()
        update_data = {"start_x": "hello_world"}
        detail_url = reverse(self.detail_url_name, kwargs={"pk": annotation.id})

        response = client.patch(detail_url, update_data)
        assert response.status_code == 400


@pytest.mark.django_db
class TestAnnotationListExternalViewSet:
    @classmethod
    def setup_class(cls) -> None:
        cls.url = reverse("annotations_external-list")

    def test_list_annotation_external(self, api_client_with_credentials: APIClient) -> None:
        client = api_client_with_credentials
        image_file = ImageFileFactory.create()
        first_annotation = AnnotationFactory.create(image_file=image_file, confirmed=True)
        second_annotation = AnnotationFactory.create(
            image_file=image_file, parent=first_annotation, confirmed=True
        )

        expected_data = [
            {
                "id": str(first_annotation.id),
                "kind": first_annotation.class_id,
                "shape": {
                    "x": [first_annotation.start_x, first_annotation.end_x],
                    "y": [first_annotation.start_y, first_annotation.end_y],
                },
                "surface": "".join(first_annotation.surface),
            },
        ]

        expected_children = [
            {
                "id": str(second_annotation.id),
                "kind": second_annotation.class_id,
                "shape": {
                    "x": [second_annotation.start_x, second_annotation.end_x],
                    "y": [second_annotation.start_y, second_annotation.end_y],
                },
                "surface": "".join(second_annotation.surface),
                "children": None,
            },
        ]

        params = {"image_file_id": image_file.id}
        response = client.get(self.url, params)

        assert response.status_code == 200
        response_data = [
            dict((k, v) for k, v in item.items() if k not in ["number", "children"])
            for item in response.data
        ]
        assert response_data == expected_data

        children = response.data[0].pop("children")
        response_data = [
            dict((k, v) for k, v in item.items() if k != "number") for item in children
        ]
        assert response_data == expected_children


@pytest.mark.django_db
class TestAnnotationListInternalViewSet:
    @classmethod
    def setup_class(cls) -> None:
        cls.url = reverse("annotations_internal-list")

    def test_list_annotation_internal(self, api_client_with_credentials: APIClient) -> None:
        client = api_client_with_credentials
        image_file = ImageFileFactory.create()
        first_annotation = AnnotationFactory.create(image_file=image_file)
        second_annotation = AnnotationFactory.create(image_file=image_file, parent=first_annotation)

        expected_data = [
            {
                "id": str(first_annotation.id),
                "class_id": first_annotation.class_id,
                "surface": first_annotation.surface,
                "shape": {
                    "end_x": first_annotation.end_x,
                    "end_y": first_annotation.end_y,
                    "start_x": first_annotation.start_x,
                    "start_y": first_annotation.start_y,
                },
                "relations": {
                    "type": first_annotation.type,
                    "label_id": None,
                },
                "meta": {
                    "confirmed": first_annotation.confirmed,
                    "confidence_percent": first_annotation.confidence_percent,
                },
            },
            {
                "id": str(second_annotation.id),
                "class_id": second_annotation.class_id,
                "surface": second_annotation.surface,
                "shape": {
                    "start_x": second_annotation.start_x,
                    "start_y": second_annotation.start_y,
                    "end_x": second_annotation.end_x,
                    "end_y": second_annotation.end_y,
                },
                "relations": {
                    "type": second_annotation.type,
                    "label_id": second_annotation.parent.id,
                },
                "meta": {
                    "confirmed": second_annotation.confirmed,
                    "confidence_percent": second_annotation.confidence_percent,
                },
            },
        ]

        params = {"image_file_id": image_file.id}
        response = client.get(self.url, params)

        assert response.status_code == 200
        response_data = [
            dict((k, v) for k, v in item.items() if k != "tags") for item in response.data
        ]
        assert response_data == expected_data
