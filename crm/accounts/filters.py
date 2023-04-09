from django_filters import CharFilter, DateFilter, FilterSet

from .models import Order


class OrderFilter(FilterSet):
    product_name = CharFilter(
        field_name='product__name', lookup_expr='icontains', label='Product'
    )
    start_date = DateFilter(
        field_name='date_created', lookup_expr='gte', label='Start date'
    )
    end_date = DateFilter(
        field_name='date_created', lookup_expr='lte', label='End date'
    )
    note = CharFilter(field_name='note', lookup_expr='icontains', label='Note')

    class Meta:
        model = Order
        fields = '__all__'
        exclude = ('product', 'customer', 'date_created')
