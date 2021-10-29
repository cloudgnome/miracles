from django.http import JsonResponse
from user.forms import UserForm
from json import loads
from catalog.models import Product

def profile(request):
    user = request.user

    form = UserForm(user.init_form(loads(request.body.decode('utf8'))),instance=user)
    if form.is_valid():
        user = form.save()

    return JsonResponse({'success':1,'data':user.dict()})

def favorites(request):
    response = [Product.objects.get(id=id).dict() for id in loads(request.body.decode('utf8'))['favorites']]

    return JsonResponse({'success':1,'data':response})