from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('user/', views.user_page, name='user_page'),
    path('account', views.account_settings, name='account'),

    path(
        'reset_password/',
        auth_views.PasswordResetView.as_view(
            template_name='password_reset.html'
        ),
        name='reset_password',
    ),
    path(
        'reset_password_sent/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='password_reset_sent.html'
        ),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/token/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='password_reset_form.html'
        ),
        name='password_reset_confirm',
    ),
    path(
        'reset_password_complete',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='password_reset_done.html'
        ),
        name='password_reset_complete',
    ),

    path('products/', views.products, name='products'),
    path('customer/<int:customer_id>/', views.customer, name='customer'),

    path('create_order/<int:customer_id>', views.create_order, name='create_order'),
    path('update_order/<int:order_id>/', views.update_order, name='update_order'),
    path('delete_order/<int:order_id>/', views.delete_order, name='delete_order'),

    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
]
