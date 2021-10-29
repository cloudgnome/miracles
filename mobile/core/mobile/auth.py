from user.auth import login
from json import loads
from mobile.forms import TokenForm
from user.models import User

def authenticate(request):
    data = loads(request.body.decode('utf8'))
    device_token = data.get('device_token')
    if not device_token:
        return {'success':0,'errors':'Авторизация не удалась.'}
    try:
        user = User.objects.get(device_token=device_token)
    except User.DoesNotExist:
        form = TokenForm(data)
        if form.is_valid():
            user = User.objects.create(device_token=device_token)
        else:
            return {'success':0,'errors':form.errors}

    login(request,user)
    data = {'success':1,'data':{'user':user.dict()}}
    data['data']['csrf_token'] = request.META['CSRF_COOKIE']

    return data