from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from payments.models import Payment
from payments.serializers import PaymentListSerializer, PaymentDetailSerializer


class PaymentViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
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
            queryset = Payment.objects.all()
            user_id_param = self.request.query_params.get("user")

            if user_id_param:
                user_ids = self._params_to_ints(user_id_param)
                queryset = queryset.filter(borrowing__user_id__in=user_ids)

        else:
            queryset = Payment.objects.filter(borrowing__user=user)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return PaymentListSerializer
        return PaymentDetailSerializer
