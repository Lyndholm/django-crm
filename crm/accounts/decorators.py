from django.contrib.auth.models import Group
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')

        return view_func(request, *args, **kwargs)

    return wrapper


def allowed_groups(groups=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_staff:
                return view_func(request, *args, **kwargs)

            groups_list = [Group.objects.get(name=group_name) for group_name in groups]
            user_groups = request.user.groups.all()

            if any(group in user_groups for group in groups_list):
                return view_func(request, *args, **kwargs)
            else:
                return redirect('home')

        return wrapper
    return decorator


def admin_only(fallback_page):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_staff:
                return view_func(request, *args, **kwargs)

            admin_group = Group.objects.get(name='admin')

            if admin_group in request.user.groups.all():
                return view_func(request, *args, **kwargs)
            else:
                return redirect(fallback_page)
        
        return wrapper
    return decorator
