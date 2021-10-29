from django.http import HttpResponse,Http404
from settings import BASE_DIR

def prom(request):
    try:
        with open(BASE_DIR + '/static/proms/%s.csv' % request.GET.get('attr'),'r') as content:
            response = HttpResponse(content=content.read(),content_type='text/csv')
    except:
        raise Http404('www')

    response['Content-Disposition'] = 'attachment; filename="prom.csv"'
    return response