from django.http import JsonResponse
from json import loads

def delete(request,Model,id = None):
    if id:
        obj = Model.objects.get(pk=id)
        obj.delete()
    else:
        for id in loads(request.body.decode('utf8')):
            obj = Model.objects.get(pk=id)
            obj.delete()

    return JsonResponse({'result':True})