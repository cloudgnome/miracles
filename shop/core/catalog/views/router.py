from catalog.views import ProductView,CategoryView,BrandView,TagView,BestsellersView,NewView,SaleView,StaticView
from catalog.models import Description,Product,Category,Brand,Tag,City,Page,Slug
from shop.views import *
from blog.views import ArticleView,ArticlesView
from blog.models import Article
from django.http import Http404,HttpResponsePermanentRedirect,HttpResponse
from shop.models import Redirect
from django.utils.http import urlunquote,http_date
from django.shortcuts import render,redirect
import os
from settings import CACHE_URL
from django.utils import timezone
from calendar import timegm
from django.db.models import Q

def resolve(request,lang='ru',slug=''):
    if hasattr(request,'LANGUAGE_CODE') and request.LANGUAGE_CODE and lang != request.LANGUAGE_CODE:
        return redirect('/%s/%s' % (request.LANGUAGE_CODE,slug))

    try:
        slug = Slug.objects.get(slug=slug)
    except Slug.DoesNotExist:
        pass

    staticDir = '{CACHE_URL}cache/html/{device}/{lang}/static/'.format(device=request.folder,lang=lang,CACHE_URL=CACHE_URL)
    if not os.path.isfile(staticDir + 'categories.html'):
        StaticView(request,staticDir)

    if slug and type(slug) != str:
        Obj = eval(slug.model)
        page = request.GET.get('page') or ''

        if Obj == Page:
            root = staticDir
            path = '{root}{path}'.format(path=slug.slug or 'index',root=root) + page
        else:
            if not slug.slug:
                raise Http404()
            if len(slug.slug) > 4:
                root = '{CACHE_URL}cache/html/{device}/{lang}/{slug[3]}/{slug[4]}/'.format(device=request.folder,lang=lang,slug=slug,CACHE_URL=CACHE_URL)
            elif len(slug.slug) > 2:
                root = '{CACHE_URL}cache/html/{device}/{lang}/{slug[1]}/{slug[2]}/'.format(device=request.folder,lang=lang,slug=slug,CACHE_URL=CACHE_URL)
            else:
                root = '{CACHE_URL}cache/html/{device}/{lang}/m/a/'.format(device=request.folder,lang=lang,slug=slug,CACHE_URL=CACHE_URL)

            path = root + str(slug).replace('/','') + request.GET.urlencode()

        path = path[:255]
        if request.is_ajax():
            path += 'ajax'

        if request.user.is_opt:
            path += 'opt'

        obj = Obj.objects.values('cached','description__last_modified').filter(pk=slug.model_id).order_by('description__last_modified').last()

        try:
            last_modified = http_date(timegm(obj.get('description__last_modified').utctimetuple()))
        except:
            last_modified = http_date(timegm(timezone.now().utctimetuple()))

        if obj and obj.get('cached') and os.path.isfile(path):
            with open(path,'rb') as content:
                if request.is_ajax() and page:
                    response = HttpResponse(content.read(),content_type="text/html")
                    response['Last-Modified'] = last_modified
                    return response
                else:
                    response = render(request,'shop/%s/index.html' % request.folder,context={'view':slug.view,'content':content.read().decode('utf8')})
                    response['Last-Modified'] = last_modified
                    return response
        elif obj:
            obj = Obj.objects.prefetch_related('description').get(pk=slug.model_id)
            last_modified = obj.description.order_by('last_modified').last()
            if not last_modified:
                last_modified = http_date(timegm(timezone.now().utctimetuple()))
            else:
                last_modified = http_date(timegm(last_modified.last_modified.utctimetuple()))

            view = eval("%sView" % slug.view).as_view()
            response = view(request,obj,lang=lang)
            obj.cached = True
            obj.update()

            if not os.path.isdir(root):
                try:
                    os.makedirs(root)
                except FileExistsError:
                    pass

            with open(path,'wb') as file:
                file.write(response.content.decode('utf8').replace('\n','').replace('\t','').encode('utf8'))

            if request.is_ajax() and page:
                response['Last-Modified'] = last_modified
                return response
            else:
                response = render(request,'shop/%s/index.html' % request.folder,context={'view':slug.view,'content':response.content.decode('utf8')})
                response['Last-Modified'] = last_modified
                return response

    try:
        permanent = Redirect.objects.get(old_path=urlunquote(slug))
        return HttpResponsePermanentRedirect('/' + (permanent.new_path or ''))
    except Redirect.DoesNotExist:
        pass

    # if not slug:
    #     return render(request,'shop/%s/index.html' % request.folder,context={'view':slug.model,'content':''})

    raise Http404('Такой страницы не существует.')