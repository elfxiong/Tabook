import json

from Tabook_models.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import User


def get_user(request, id):
    user = None
    if request.method == 'GET':
        user = get_object_or_404(User, id=id)

    content = {'id': user.id, 'username': user.username, 'email': user.email, 'phone': user.phone}
    return HttpResponse(content=json.dumps(content), content_type="application/json")


@csrf_exempt
def create_user(request):
    content = {'success': False}
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            content['success'] = True
            content['id'] = user.id
        else:
            content['result'] = "Failed to create a new user"
            content['html'] = form.errors
    else:
        content['result'] = "Invalid request method"
        pass  # do no respond
    return HttpResponse(content=json.dumps(content), content_type="application/json")
