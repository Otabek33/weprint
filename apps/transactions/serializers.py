from rest_framework import serializers

from apps.orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['uuid', 'order_number', 'price']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Filter the fields you want to include in the representation
        filtered_data = {key: value for key, value in data.items() if key in ['uuid', 'order_number', 'price']}
        return filtered_data
