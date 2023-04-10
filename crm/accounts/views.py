from django.contrib import messages
from django.forms import inlineformset_factory
from django.shortcuts import redirect, render

from .filters import OrderFilter
from .forms import CreateOrderForm, CreateUserForm
from .models import Customer, Order, Product


def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {
        'orders': orders,
        'customers': customers,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending,
    }
    return render(request, 'accounts/dashboard.html', context)


def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})


def customer(request, customer_id):
    customer = Customer.objects.get(id=customer_id)

    orders = customer.order_set.all()
    order_count = orders.count()

    orders_filter = OrderFilter(request.GET, queryset=orders)
    orders = orders_filter.qs

    context = {
        'customer': customer,
        'orders': orders,
        'order_count': order_count,
        'orders_filter': orders_filter,
    }
    return render(request, 'accounts/customer.html', context)


def create_order(request, customer_id):
    OrderFormSet = inlineformset_factory(
        Customer, Order, fields=('product', 'status'), extra=3
    )

    customer = Customer.objects.get(id=customer_id)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)

    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset': formset}
    return render(request, 'accounts/order_form.html', context)


def update_order(request, order_id):
    order = Order.objects.get(id=order_id)
    form = CreateOrderForm(instance=order)

    if request.method == 'POST':
        form = CreateOrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


def delete_order(request, order_id):
    order = Order.objects.get(id=order_id)

    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'item': order}
    return render(request, 'accounts/delete.html', context)


def register_page(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()

            user = form.cleaned_data.get('username')
            messages.success(request, f'Account was created for {user}')

            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def login_page(request):
    context = {}
    return render(request, 'accounts/login.html', context)
