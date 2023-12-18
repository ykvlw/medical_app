from typing import TYPE_CHECKING, Any, Optional, Type, Union

from rest_framework.serializers import Serializer
from rest_framework.viewsets import GenericViewSet

BaseViewMixinBaseClass: Type[Union[object, GenericViewSet]] = (
    object if not TYPE_CHECKING else GenericViewSet
)

UPDATE_ACTIONS = (
    "update",
    "partial_update",
    "partial_update_bulk",
    "update_bulk",
)


class BaseSchemaMixin:
    _representation: Optional[Serializer] = None

    def set_representation(self, serializer: Serializer) -> None:
        self._representation = serializer

    def get_representation(self) -> Optional[Serializer]:
        return self._representation

    def to_representation(self, instance: Any) -> dict:
        if self._representation:
            return self._representation.to_representation(instance)
        return super().to_representation(instance)  # type: ignore


class BaseViewMixin(BaseViewMixinBaseClass):
    schema_class: Optional[Type[Serializer]] = None
    schema_update_class: Optional[Type[Serializer]] = None
    serializer_list_class: Optional[Type[Serializer]] = None
    serializer_create_class: Optional[Type[Serializer]] = None
    serializer_retrieve_class: Optional[Type[Serializer]] = None

    def _get_serializer_class(self) -> Optional[Type[Serializer]]:
        if self.action == "create":
            return self.schema_class
        if self.action in UPDATE_ACTIONS:
            return self.schema_update_class or self.schema_class
        if self.action == "retrieve":
            return self.serializer_retrieve_class or self.serializer_class
        if self.action == "list":
            return self.serializer_list_class or self.serializer_class
        return None

    def get_serializer_class(self, *args: Any, **kwargs: Any) -> Type[Serializer]:
        serializer_class = self._get_serializer_class()
        if serializer_class is not None:
            return serializer_class
        return super().get_serializer_class(*args, **kwargs)

    def get_presentation_class(self) -> Optional[Type[Serializer]]:
        default = super().get_serializer_class()
        if self.action == "create":
            return self.serializer_create_class or default
        return default

    def get_serializer(self, *args: Any, **kwargs: Any) -> Serializer:
        serializer_class = self.get_serializer_class()
        kwargs["context"] = self.get_serializer_context()
        serializer: Serializer = serializer_class(*args, **kwargs)
        if isinstance(serializer, BaseSchemaMixin):
            presentation_class = self.get_presentation_class()
            if presentation_class:
                serializer.set_representation(presentation_class(*args, **kwargs))
        return serializer
