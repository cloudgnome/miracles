from django.http import JsonResponse

def change_database(request):
    request.session['database'] = request.GET.get('database')

    return JsonResponse({'result':True})