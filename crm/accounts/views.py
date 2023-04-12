from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.forms import inlineformset_factory
from django.shortcuts import redirect, render

from .decorators import admin_only, allowed_groups, unauthenticated_user
from .filters import OrderFilter
from .forms import CreateOrderForm, CreateUserForm, CustomerForm
from .models import Customer, Order, Product


@login_required(login_url='login')
@admin_only(fallback_page='user_page')
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


@allowed_groups(groups=['admin'])
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})


@login_required(login_url='login')
@allowed_groups(groups=['admin'])
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


@login_required(login_url='login')
@allowed_groups(groups=['customer'])
def user_page(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {
        'orders': orders,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending,
    }
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_groups(groups=['customer'])
def account_settings(request):
    user = request.user.customer
    form = CustomerForm(instance=user)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'accounts/account_settings.html', context)


@login_required(login_url='login')
@allowed_groups(groups=['admin'])
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


@login_required(login_url='login')
@allowed_groups(groups=['admin'])
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


@login_required(login_url='login')
@allowed_groups(groups=['admin'])
def delete_order(request, order_id):
    order = Order.objects.get(id=order_id)

    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'item': order}
    return render(request, 'accounts/delete.html', context)


@unauthenticated_user
def register_page(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, f'Account was created for {username}')

            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Invalid credentials')

    context = {}
    return render(request, 'accounts/login.html', context)


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('home')
