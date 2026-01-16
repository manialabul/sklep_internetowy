from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def starts_with(self, request):
        """
        Endpoint: /api/products/starts_with/?letter=L
        Zwraca produkty zaczynające się od podanej litery
        """
        letter = request.query_params.get('letter', None)
        if not letter:
            return Response({"error": "Musisz podać parametr 'letter'"}, status=400)
        products = Product.objects.filter(name__istartswith=letter)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Każdy użytkownik widzi tylko swoje zamówienia
        """
        user = self.request.user
        return Order.objects.filter(user=user)

    @action(detail=False, methods=['get'])
    def my_orders(self, request):
        """
        Endpoint: /api/orders/my_orders/
        Pokazuje wszystkie zamówienia zalogowanego użytkownika
        """
        orders = self.get_queryset()
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def monthly_summary(self, request):
        """
        Endpoint: /api/orders/monthly_summary/?month=1&year=2026
        Zwraca liczbę zamówień w danym miesiącu
        """
        from django.db.models import Count
        from datetime import datetime

        month = int(request.query_params.get('month', datetime.today().month))
        year = int(request.query_params.get('year', datetime.today().year))
        orders = Order.objects.filter(created_at__year=year, created_at__month=month)
        return Response({"month": month, "year": year, "orders_count": orders.count()})