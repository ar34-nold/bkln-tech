from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Notification


@login_required
def notification_list(request):
    return render(request, "generic/list.html", {"title": "Notifications", "objects": Notification.objects.filter(user=request.user), "fields": ["title", "channel", "read", "created_at"]})

# Create your views here.
