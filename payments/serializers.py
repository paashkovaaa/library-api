from rest_framework import serializers

from payments.models import Payment


class PaymentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            "id",
            "status",
            "type",
            "borrowing",
            "session_id",
            "session_url",
            "money_to_pay",
        )


class PaymentListSerializer(PaymentDetailSerializer):
    class Meta:
        model = Payment
        fields = ("id", "status", "borrowing", "money_to_pay")
