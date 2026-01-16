from rest_framework import serializers
from .models import Product, Order, OrderItem
from datetime import date


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Cena musi być większa od 0")
        return value


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    def validate_delivery_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("Data nie może być z przeszłości")
        return value
