import json

from Tabook_models.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import User


def reset_user_info(request):
    content = {'success': False}
    if request.method == "POST":
        if request.POST['id']:
            try:
                id = request.POST['id']
                u = User.objects.get(pk=id)
                if 'username' in request.POST:
                    username = request.POST['username']
                    u.username = username
                    u.save()
                    content['success'] = True
                if 'email' in request.POST:
                    email = request.POST['email']
                    u.email = email
                    u.save()
                    content['success'] = True
                if 'phone' in request.POST:
                    phone = request.POST['phone']
                    u.phone = phone
                    u.save()
                    content['success'] = True
            except:
                content['result'] = "User not found"
        else:
            content['result'] = "User id not provided"
    else:
        content['result'] = "Invalid request method"

    return HttpResponse(content=json.dumps(content), content_type="application/json")



def get_user(request, id):
    user = None
    content = {"success":False}
    if request.method == 'GET':
        try:
            user = User.objects.get(pk=id)
            content["success"] = True
            for key,value in {'id': user.id, 'username': user.username, 'email': user.email, 'phone': user.phone}.items():
                content[key] = value
        except:
            content["result"] = "user not found"

    return HttpResponse(content=json.dumps(content), content_type="application/json")


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
