import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import User


def get_user(request, id):
    user = None
    if request.method == 'GET':
        user = get_object_or_404(User, id=id)

    content = {'id': user.id, 'username': user.username, 'email': user.email, 'phone': user.phone}
    return HttpResponse(content=json.dumps(content), content_type="application/json")
