from django.shortcuts import render
from .models import User


def counter(request):
    user_count = User.objects.count()
    context = {'user_count': user_count}
    return render(request, 'user_count.html', context)
