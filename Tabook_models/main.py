from Tabook_models.forms import UserCreationForm
from django.http import JsonResponse
from .models import User


def reset_user_info(request):
    content = {'success': False}
    if request.method == "POST":
        if request.POST['id']:
            try:
                uid = request.POST['id']
                user = User.objects.get(pk=uid)
            except User.DoesNotExist:
                content['result'] = "User not found"
            else:
                content['changed'] = []
                if 'username' in request.POST:
                    username = request.POST['username']
                    user.username = username
                    content['changed'] += 'username'
                if 'email' in request.POST:
                    email = request.POST['email']
                    user.email = email
                    content['changed'] += 'email'
                if 'phone' in request.POST:
                    phone = request.POST['phone']
                    user.phone = phone
                    content['changed'] = 'phone'
                user.save()
                content['success'] = True
        else:
            content['result'] = "User id not provided"
    else:
        content['result'] = "Invalid request method"
    return JsonResponse(content)


def get_user(request, id):
    content = {"success": False}
    if request.method == 'GET':
        try:
            user = User.objects.get(pk=id)
        except User.DoesNotExist:
            content["result"] = "user not found"
        else:
            content["success"] = True
            for key, value in {'id': user.id, 'username': user.username, 'email': user.email,
                               'phone': user.phone}.items():
                content[key] = value
    return JsonResponse(content)


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
    return JsonResponse(content)
