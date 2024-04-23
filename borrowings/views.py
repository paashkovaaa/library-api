from datetime import date

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingListSerializer,
    BorrowingDetailSerializer,
    BorrowingCreateSerializer,
)


class BorrowingViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    permission_classes = [
        IsAuthenticated,
    ]

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            queryset = Borrowing.objects.all()
            user_id_param = self.request.query_params.get("user")

            if user_id_param:
                user_ids = self._params_to_ints(user_id_param)
                queryset = queryset.filter(user_id__in=user_ids)

        else:
            queryset = Borrowing.objects.filter(user=user)

        is_active_param = self.request.query_params.get("is_active")
        if is_active_param:
            is_active_bool = is_active_param.lower() in ["true", "1"]
            queryset = queryset.filter(actual_return_date__isnull=is_active_bool)

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "is_active",
                type=OpenApiTypes.BOOL,
                description="Filter by is_active field (ex. ?is_active=True)",
            ),
            OpenApiParameter(
                "user",
                type=OpenApiTypes.INT,
                description="Filter by user id, only for admin (ex. ?user=1)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        if not request.user.is_staff and "user" in request.query_params:
            return Response(
                {"detail": "You do not have permission to use 'user' filter."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer
        elif self.action == "create":
            return BorrowingCreateSerializer
        return BorrowingDetailSerializer

    @extend_schema(
        request=None,
    )
    @action(
        detail=True, methods=["post"], url_path="return", url_name="return_borrowing"
    )
    def return_borrowing(self, request, pk=None):
        borrowing = self.get_object()
        if borrowing.actual_return_date:
            return Response(
                {"detail": "This borrowing has already been returned."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        borrowing.actual_return_date = date.today()
        borrowing.book.inventory += 1
        borrowing.book.save()
        borrowing.save()

        return Response(
            {"detail": "Borrowing returned successfully."},
            status=status.HTTP_200_OK,
        )
